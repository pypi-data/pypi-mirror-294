"""Models."""

from math import ceil
from typing import Dict, Set

from moonmining.models import Moon as MoonminigMoon

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Min, Sum
from django.utils import timezone
from esi.models import Token
from eveuniverse.models import EveGroup, EveMoon, EveType

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

from metenox.app_settings import METENOX_MOON_MATERIAL_BAY_CAPACITY

ESI_SCOPES = [
    "esi-universe.read_structures.v1",
    "esi-corporations.read_structures.v1",
    "esi-assets.read_corporation_assets.v1",
]

logger = get_extension_logger(__name__)


class General(models.Model):
    """A meta model for app permissions."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access this app"),
            ("auditor", "Can access metenox information about all corporations"),
        )


class HoldingCorporation(models.Model):
    """Corporation holding metenox moon drills"""

    corporation = models.OneToOneField(
        EveCorporationInfo, on_delete=models.CASCADE, primary_key=True
    )

    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(null=True, default=None)

    @property
    def alliance(self):
        """Returns holding corp's alliance"""
        return self.corporation.alliance

    @property
    def corporation_name(self):
        """Returns the holding corporation's name"""
        return self.corporation.corporation_name

    @property
    def count_metenoxes(self) -> int:
        """Return the number of metenoxes a holding corporation owns"""
        return self.metenoxes.count()

    @property
    def raw_revenue(self) -> float:
        """Returns the raw metenox revenus before fuel prices"""
        return self.metenoxes.aggregate(Sum("moon__value"))["moon__value__sum"]

    @property
    def profit(self) -> float:
        """Returns the metenoxes profit after fuel prices"""
        if self.raw_revenue:
            return self.raw_revenue - self.count_metenoxes * Moon.fuel_price()
        return 0.0

    def __str__(self) -> str:
        return self.corporation_name


class Owner(models.Model):
    """Character in corporation owning metenoxes"""

    corporation = models.ForeignKey(
        HoldingCorporation,
        on_delete=models.CASCADE,
        related_name="owners",
    )

    character_ownership = models.ForeignKey(
        CharacterOwnership,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="+",
        help_text="Character used to sync this corporation from ESI",
    )

    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Disabled corporations are excluded from the update process",
    )

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        """Return name."""
        alliance_ticker_str = (
            f" [{self.corporation.alliance.alliance_ticker}]"
            if self.corporation.alliance
            else ""
        )
        return f"{self.corporation}{alliance_ticker_str} - {self.character_ownership.character}"

    @property
    def alliance_name(self) -> str:
        """Return alliance name."""
        return (
            self.corporation.alliance.alliance_name if self.corporation.alliance else ""
        )

    def fetch_token(self) -> Token:
        """Return valid token for this mining corp or raise exception on any error."""
        if not self.character_ownership:
            raise RuntimeError("This owner has no character configured.")
        token = (
            Token.objects.filter(
                character_id=self.character_ownership.character.character_id
            )
            .require_scopes(ESI_SCOPES)
            .require_valid()
            .first()
        )
        if not token:
            raise Token.DoesNotExist(f"{self}: No valid token found.")
        return token

    @classmethod
    def get_owners_associated_to_user(cls, user: User):
        """Returns all owners of the user"""
        return cls.objects.filter(character_ownership__user=user)


class Moon(models.Model):
    """Represents a moon and the metenox related values"""

    __HOURLY_MAGMATIC = 55
    __HOURLY_FUEL_BLOCKS = 5

    eve_moon = models.OneToOneField(
        EveMoon, on_delete=models.CASCADE, primary_key=True, related_name="+"
    )

    moonmining_moon = models.OneToOneField(
        MoonminigMoon,
        on_delete=models.CASCADE,
        null=True,  # metenox might be dropped on an unknown moon
        default=None,
        related_name="+",
    )

    value = models.FloatField(default=0)
    value_updated_at = models.DateTimeField(null=True, default=None)

    @property
    def hourly_pull(self) -> Dict[EveType, int]:
        """Returns how much goo is harvested in an hour by a metenox"""
        hourly_products = MetenoxHourlyProducts.objects.filter(moon=self)
        return {product.product: product.amount for product in hourly_products}

    @property
    def name(self) -> str:
        """Returns name of this moon"""
        return self.eve_moon.name.replace("Moon ", "")

    @property
    def rarity_class(self):
        """Returns rarity class of this moon"""
        return self.moonmining_moon.rarity_class

    def update_price(self):
        """Updates the Metenox price attribute to display"""
        hourly_harvest_value = sum(
            EveTypePrice.get_eve_type_price(moon_goo) * moon_goo_amount
            for moon_goo, moon_goo_amount in self.hourly_pull.items()
        )
        self.value = hourly_harvest_value * 24 * 30
        self.value_updated_at = timezone.now()
        self.save()

    @property
    def cycles_before_full(self) -> int:
        """Number of harvest cycles before the moon material bay is at full capacity"""
        bay_capacity = METENOX_MOON_MATERIAL_BAY_CAPACITY
        harvest_volume = sum(
            goo_type.volume * amount for goo_type, amount in self.hourly_pull.items()
        )
        return ceil(bay_capacity / harvest_volume)

    @classmethod
    def fuel_price(cls) -> float:
        """Returns the monthly price of running a metenox"""
        hourly_price = (
            cls.__HOURLY_MAGMATIC * EveTypePrice.get_magmatic_gases_price()
            + cls.__HOURLY_FUEL_BLOCKS * EveTypePrice.get_fuel_block_price()
        )
        return hourly_price * 24 * 30

    def profit(self) -> float:
        """Returns the monthly profit of a meteneox including the fuel price"""
        return self.value - self.fuel_price()

    def __str__(self):
        return self.name


class Metenox(models.Model):
    """
    Represents a metenox anchored on a moon
    """

    structure_id = models.PositiveBigIntegerField(primary_key=True)
    structure_name = models.TextField(max_length=150)

    moon = models.OneToOneField(
        Moon,
        on_delete=models.CASCADE,
        related_name="metenox",
    )
    corporation = models.ForeignKey(
        HoldingCorporation, on_delete=models.CASCADE, related_name="metenoxes"
    )

    fuel_blocks_count = models.IntegerField(default=0)
    magmatic_gas_count = models.IntegerField(default=0)

    def __str__(self):
        return self.structure_name

    class Meta:
        verbose_name_plural = "Metenoxes"


class MetenoxHourlyProducts(models.Model):
    """
    Represents how much moon goo a Metenox harvests in an hour
    """

    moon = models.ForeignKey(Moon, on_delete=models.CASCADE, related_name="+")
    product = models.ForeignKey(EveType, on_delete=models.CASCADE, related_name="+")

    amount = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.amount}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["moon", "product"], name="functional_pk_metenoxhourlyproduct"
            )
        ]

    @classmethod
    def all_moon_goo_ids(cls) -> Set[int]:
        """Returns all known moon goo ids in the database"""
        return set(cls.objects.values_list("product", flat=True).order_by("product_id"))


class EveTypePrice(models.Model):
    """
    Represent an eve type and its last fetched price
    """

    __MOON_GOOS_GROUP_ID = 427
    __FUEL_BLOCK_GROUP_ID = 1136
    __MAGMATIC_TYPE_ID = 81143

    eve_type = models.OneToOneField(EveType, on_delete=models.CASCADE, related_name="+")
    price = models.FloatField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.eve_type.name} - {self.price} ISK"

    def update_price(self, new_price: float):
        """Updates the price of an item"""
        self.price = new_price
        self.save()

    @classmethod
    def get_eve_type_price(cls, eve_type: EveType) -> float:
        """Returns the price of an item"""
        type_price, _ = cls.objects.get_or_create(eve_type=eve_type)
        return type_price.price

    @classmethod
    def get_eve_type_id_price(cls, eve_type_id: int) -> float:
        """Returns the price of an item id"""
        return cls.get_eve_type_price(EveType.objects.get(id=eve_type_id))

    @classmethod
    def _get_type_ids_from_group(cls, group_id: int) -> Set[int]:
        """Fetches type ids from their group and returns it as a set"""
        group = EveGroup.objects.get(id=group_id)
        return set(group.eve_types.filter(published=True).values_list("id", flat=True))

    @classmethod
    def get_fuels_type_ids(cls) -> Set[int]:
        """Fetches the id of all 4 fuel blocks from their group and magmatic gas"""
        return cls._get_type_ids_from_group(cls.__FUEL_BLOCK_GROUP_ID) | {
            cls.__MAGMATIC_TYPE_ID
        }

    @classmethod
    def get_moon_goos_type_ids(cls) -> Set[int]:
        """Fetches the ids of all moon goos from their group"""
        return cls._get_type_ids_from_group(cls.__MOON_GOOS_GROUP_ID)

    @classmethod
    def get_magmatic_gas_type_id(cls) -> int:
        """Return the type of magmatic gases"""
        return cls.__MAGMATIC_TYPE_ID

    @classmethod
    def get_fuel_block_price(cls):
        """Returns the price of the cheapest fuel block"""
        return cls.objects.filter(
            eve_type__eve_group=cls.__FUEL_BLOCK_GROUP_ID
        ).aggregate(Min("price"))["price__min"]

    @classmethod
    def get_magmatic_gases_price(cls) -> float:
        """Returns the price of a unit of magmatic gases"""
        return cls.get_eve_type_id_price(cls.__MAGMATIC_TYPE_ID)
