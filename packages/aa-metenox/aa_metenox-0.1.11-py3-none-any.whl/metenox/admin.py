"""Admin site."""

from django.contrib import admin

from metenox.models import EveTypePrice, HoldingCorporation, Metenox, Moon
from metenox.templatetags.metenox import formatisk


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ["name", "moon_value", "value_updated_at"]
    fields = [("eve_moon", "moonmining_moon"), ("value", "value_updated_at")]
    search_fields = ["eve_moon__name"]
    readonly_fields = ["eve_moon", "moonmining_moon"]

    @admin.display(description="value")
    def moon_value(self, moon: Moon):
        return f"{formatisk(moon.value)} ISK"

    # TODO add harvested materials


@admin.register(Metenox)
class MetenoxAdmin(admin.ModelAdmin):
    list_display = [
        "structure_name",
        "corporation",
        "metenox_value",
        "fuel_blocks_count",
        "magmatic_gas_count",
    ]
    fields = [
        ("structure_id", "structure_name"),
        "moon",
        "corporation",
        ("fuel_blocks_count", "magmatic_gas_count"),
    ]
    readonly_fields = ["structure_id", "moon"]

    @admin.display(description="value")
    def metenox_value(self, metenox: Metenox):
        return f"{formatisk(metenox.moon.value)} ISK"


@admin.register(HoldingCorporation)
class HoldingCorporationAdmin(admin.ModelAdmin):
    list_display = ["corporation", "is_active", "count_metenox"]
    readonly_fields = ["corporation", "last_updated", "count_metenox"]

    @admin.display(description="Number metenoxes")
    def count_metenox(self, holding: HoldingCorporation) -> int:
        return holding.count_metenoxes


@admin.register(EveTypePrice)
class EveTypePriceAdmin(admin.ModelAdmin):
    list_display = ["eve_type", "type_price"]
    readonly_fields = ["eve_type", "last_update"]

    @admin.display(description="Price")
    def type_price(self, type_price: EveTypePrice):
        return f"{formatisk(type_price.price)} ISK"
