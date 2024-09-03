"""Tasks."""

from typing import Optional

from celery import shared_task
from moonmining.constants import EveTypeId
from moonmining.models.moons import Moon as MoonminingMoon

from eveuniverse.constants import EveGroupId
from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from metenox.api.fuzzwork import BuySell, get_type_ids_prices
from metenox.esi import (
    get_corporation_metenox_assets,
    get_metenox_from_esi,
    get_structure_info_from_esi,
)
from metenox.models import (
    EveTypePrice,
    HoldingCorporation,
    Metenox,
    MetenoxHourlyProducts,
    Moon,
)
from metenox.moons import get_metenox_hourly_harvest

logger = get_extension_logger(__name__)


class TaskError(Exception):
    """To be raised when a task fails"""


@shared_task
def update_holding(holding_corp_id: int):
    """
    Updated the list of metenoxes under a specific owner
    If harvest is set to True the harvest components are also recalculated
    """

    logger.info("Updating corporation id %s", holding_corp_id)

    holding_corp = HoldingCorporation.objects.get(
        corporation__corporation_id=holding_corp_id
    )

    metenoxes_info = get_metenox_from_esi(holding_corp)
    if not metenoxes_info:
        logger.warning("Failed to fetch the metenoxes for corporation %s", holding_corp)
        raise TaskError
    metenoxes_info_dic = {
        metenox["structure_id"]: metenox for metenox in metenoxes_info
    }

    metenoxes_ids = set(metenox["structure_id"] for metenox in metenoxes_info)

    metenoxes_asset_dic = get_corporation_metenox_assets(holding_corp, metenoxes_ids)

    current_metenoxes_ids = set(
        metenox.structure_id
        for metenox in Metenox.objects.filter(corporation=holding_corp)
    )

    disappeared_metenoxes_ids = (
        current_metenoxes_ids - metenoxes_ids
    )  # metenoxes that have been unanchored/destroyed/transferred
    Metenox.objects.filter(structure_id__in=disappeared_metenoxes_ids).delete()

    missing_metenoxes_ids = metenoxes_ids - current_metenoxes_ids
    for metenox_id in missing_metenoxes_ids:
        location_info = get_structure_info_from_esi(holding_corp, metenox_id)
        create_metenox.delay(
            holding_corp.corporation.corporation_id,
            metenoxes_info_dic[metenox_id],
            location_info,
        )

    metenoxes_to_updates = (
        current_metenoxes_ids - disappeared_metenoxes_ids - missing_metenoxes_ids
    )
    for metenox_id in metenoxes_to_updates:
        update_metenox.delay(
            metenox_id, metenoxes_info_dic[metenox_id], metenoxes_asset_dic[metenox_id]
        )


@shared_task
def create_metenox(
    holding_corporation_id: int, structure_info: dict, location_info: dict
):
    """
    Creates and adds the Metenox in the database
    """
    holding_corporation = HoldingCorporation.objects.get(
        corporation__corporation_id=holding_corporation_id
    )
    logger.info(
        "Creating metenox %s for %s",
        structure_info["structure_id"],
        holding_corporation,
    )
    solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
        id=location_info["solar_system_id"]
    )
    try:
        nearest_celestial = solar_system.nearest_celestial(
            x=location_info["position"]["x"],
            y=location_info["position"]["y"],
            z=location_info["position"]["z"],
            group_id=EveGroupId.MOON,
        )
    except OSError as exc:
        logger.exception("%s: Failed to fetch nearest celestial", structure_info)
        raise exc

    if not nearest_celestial or nearest_celestial.eve_type.id != EveTypeId.MOON:
        logger.exception(
            "Couldn't find the moon corresponding to metenox %s", structure_info
        )
        raise TaskError

    eve_moon = nearest_celestial.eve_object
    moon, _ = Moon.objects.get_or_create(eve_moon=eve_moon)

    metenox = Metenox(
        moon=moon,
        structure_name=structure_info["name"],
        structure_id=structure_info["structure_id"],
        corporation=holding_corporation,
    )
    metenox.save()


@shared_task()
def update_metenox(
    metenox_structure_id: int,
    structure_info: dict,
    metenox_assets: Optional[list[dict]] = None,
):
    """
    Updates a metenox already existing in the database. Already receives the fetched ESI information of the structure
    """

    logger.info("Updating metenox id %s", metenox_structure_id)

    metenox = Metenox.objects.get(structure_id=metenox_structure_id)

    if metenox.structure_name != structure_info["name"]:
        logger.info("Updating metenox id %s name", metenox_structure_id)
        metenox.structure_name = structure_info["name"]

    metenox.fuel_blocks_count = 0
    for asset in metenox_assets:
        if asset["location_flag"] == "StructureFuel":
            if asset["type_id"] == EveTypePrice.get_magmatic_gas_type_id():
                metenox.magmatic_gas_count = asset["quantity"]
            elif asset["type_id"] in EveTypePrice.get_fuels_type_ids():
                metenox.fuel_blocks_count += asset["quantity"]
        # TODO update moongoobay

    metenox.save()


@shared_task
def update_moon(moon_id: int, update_materials: bool = False):
    """
    Update the materials and price of a Moon
    If update_materials is set to true it will look in the moonmining app to update the composition
    """
    logger.info("Updating price of moon id %s", moon_id)

    moon = Moon.objects.get(eve_moon_id=moon_id)

    moon.update_price()

    # TODO write a test for this
    if update_materials:

        # clears the previous harvested materials
        Metenox.objects.filter(moon=moon).delete()

        create_moon_materials(moon_id)


@shared_task
def create_moon_materials(moon_id: int):
    """
    Creates the materials of a moon without materials yet
    """

    moon = Moon.objects.get(eve_moon_id=moon_id)

    harvest = get_metenox_hourly_harvest(moon_id)

    MetenoxHourlyProducts.objects.bulk_create(
        [
            MetenoxHourlyProducts(moon=moon, product=goo_type, amount=amount)
            for goo_type, amount in harvest.items()
        ],
        update_conflicts=True,
        unique_fields=["moon", "product"],
        update_fields=["amount"],
    )

    moon.update_price()


@shared_task
def update_moons_from_moonmining(*, no_delay=False):
    """
    Will fetch all the moons from aa-moonmining application and update the metenox database

    no_delay is a param for testing purpose to disable task delaying and make sure everything is synchronous
    """

    logger.info("Updating all moons from moonming")

    metenox_moons = Moon.objects.all()
    metenox_moon_ids = [moon.eve_moon.id for moon in metenox_moons]
    missing_moons = MoonminingMoon.objects.exclude(eve_moon__id__in=metenox_moon_ids)

    for moon in missing_moons:
        if no_delay:
            create_moon_from_moonmining(moon.eve_moon.id)
        else:
            create_moon_from_moonmining.delay(moon.eve_moon.id)

    # creates data for moons that are missing their pulls
    moons_to_update = [moon for moon in metenox_moons if len(moon.hourly_pull) == 0]
    for moon in moons_to_update:
        if no_delay:
            create_moon_materials(moon.eve_moon.id)
        else:
            create_moon_materials.delay(moon.eve_moon.id)


@shared_task
def create_moon_from_moonmining(moon_id: int):
    """
    Fetches a moon from moonmining. Creates it for metenox and fetches materials
    """

    logger.info("Updating materials of moon id %s", moon_id)

    Moon.objects.get_or_create(
        eve_moon_id=moon_id,
        moonmining_moon=MoonminingMoon.objects.get(eve_moon_id=moon_id),
    )

    create_moon_materials(moon_id)


@shared_task
def update_prices():
    """Task fetching prices and then updating all moon values"""

    goo_ids = EveTypePrice.get_moon_goos_type_ids()

    goo_prices = get_type_ids_prices(goo_ids)

    for type_id, price in goo_prices.items():
        type_price, _ = EveTypePrice.objects.get_or_create(
            eve_type_id=type_id,
        )
        type_price.update_price(price)

    fuel_ids = EveTypePrice.get_fuels_type_ids()
    fuel_prices = get_type_ids_prices(fuel_ids, BuySell.SELL)

    for type_id, price in fuel_prices.items():
        type_price, _ = EveTypePrice.objects.get_or_create(
            eve_type_id=type_id,
        )
        type_price.update_price(price)

    moons = Moon.objects.all()
    logger.info(
        "Successfully updated goo and fuel prices. Now updating %s moons", moons.count()
    )

    for moon in moons:
        update_moon.delay(moon.eve_moon_id)
