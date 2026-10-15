"""Number entities for IntelliCharge."""

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

DOMAIN = "intellicharge"


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            IntelliChargeMinSocAfterSell(coordinator),
            IntelliChargeMaxBatterySoc(coordinator),
            IntelliChargeMinBatterySoc(coordinator),
            IntelliChargeMaxCharge(coordinator),
            IntelliChargeMaxDischarge(coordinator),
        ]
    )


class IntelliChargeBaseNumber(
    CoordinatorEntity,
    NumberEntity,
):
    field_name = None

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def rules(self):
        return self.coordinator.data.get(
            "charging_rules",
            [],
        )

    def _get_rule(self):
        if not self.rules:
            return None

        return dict(self.rules[0])

    async def async_set_native_value(
        self,
        value,
    ):
        rule = self._get_rule()

        if not rule:
            return

        rule[self.field_name] = int(value)

        await self.coordinator.api.async_set_custom_charging_rules(
            [rule]
        )

        await self.coordinator.async_request_refresh()


class IntelliChargeMinSocAfterSell(
    IntelliChargeBaseNumber,
):
    field_name = "min_battery_soc_for_sell"

    _attr_name = "Min SOC After Sell"
    _attr_unique_id = (
        "intellicharge_min_soc_after_sell"
    )

    _attr_native_min_value = 10
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        if not self.rules:
            return 10

        return self.rules[0].get(
            self.field_name,
            10,
        )


class IntelliChargeMaxBatterySoc(
    IntelliChargeBaseNumber,
):
    field_name = "max_battery_soc"

    _attr_name = "Max Battery SOC"
    _attr_unique_id = (
        "intellicharge_max_battery_soc"
    )

    _attr_native_min_value = 10
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        if not self.rules:
            return 100

        value = self.rules[0].get(
            self.field_name
        )

        return (
            value
            if value is not None
            else 100
        )


class IntelliChargeMinBatterySoc(
    IntelliChargeBaseNumber,
):
    field_name = "min_battery_soc"

    _attr_name = "Min Battery SOC"
    _attr_unique_id = (
        "intellicharge_min_battery_soc"
    )

    _attr_native_min_value = 10
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        if not self.rules:
            return 10

        value = self.rules[0].get(
            self.field_name
        )

        return (
            value
            if value is not None
            else 10
        )


class IntelliChargeMaxCharge(
    IntelliChargeBaseNumber,
):
    field_name = "max_charge"

    _attr_name = "Max Charge"
    _attr_unique_id = (
        "intellicharge_max_charge"
    )

    _attr_native_min_value = 0
    _attr_native_max_value = 20000
    _attr_native_step = 100
    _attr_native_unit_of_measurement = "W"

    @property
    def native_value(self):
        if not self.rules:
            return 0

        value = self.rules[0].get(
            self.field_name
        )

        return (
            value
            if value is not None
            else 0
        )


class IntelliChargeMaxDischarge(
    IntelliChargeBaseNumber,
):
    field_name = "max_discharge"

    _attr_name = "Max Discharge"
    _attr_unique_id = (
        "intellicharge_max_discharge"
    )

    _attr_native_min_value = 0
    _attr_native_max_value = 20000
    _attr_native_step = 100
    _attr_native_unit_of_measurement = "W"

    @property
    def native_value(self):
        if not self.rules:
            return 0

        value = self.rules[0].get(
            self.field_name
        )

        return (
            value
            if value is not None
            else 0
        )
