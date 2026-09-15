"""Number entities for IntelliCharge."""

from homeassistant.components.number import (
    NumberEntity,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from . import IntelliChargeDataUpdateCoordinator

DOMAIN = "intellicharge"


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            IntelliChargeMinSocAfterSell(
                coordinator
            )
        ]
    )


class IntelliChargeMinSocAfterSell(
    CoordinatorEntity,
    NumberEntity,
):
    """Minimum battery SOC after sell."""

    _attr_name = "Min SOC After Sell"

    _attr_native_min_value = 10
    _attr_native_max_value = 100
    _attr_native_step = 1

    _attr_native_unit_of_measurement = "%"

    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_unique_id = (
            "intellicharge_min_soc_after_sell"
        )

    @property
    def native_value(self):

        rules = self.coordinator.data.get(
            "charging_rules",
            [],
        )

        if not rules:
            return 10

        return (
            rules[0].get(
                "min_battery_soc_for_sell",
                10,
            )
        )

    async def async_set_native_value(
        self,
        value,
    ):
        rule = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": True,
            "sunday": True,
            "valid_from": "00:00:00",
            "valid_to": "23:59:59",
            "max_charge": None,
            "max_discharge": None,
            "max_battery_soc": None,
            "min_battery_soc": None,
            "min_battery_soc_for_sell": int(value),
        }

        await self.coordinator.api.async_set_custom_charging_rules(
            [rule]
        )

        await self.coordinator.async_request_refresh()