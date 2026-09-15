"""Sensor platform for IntelliCharge."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "intellicharge"


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            IntelliChargeChargingRulesSensor(
                coordinator
            )
        ]
    )


class IntelliChargeChargingRulesSensor(
    CoordinatorEntity,
    SensorEntity,
):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = (
            "IntelliCharge Charging Rules"
        )

        self._attr_unique_id = (
            "intellicharge_charging_rules"
        )

    @property
    def native_value(self):
        rules = self.coordinator.data.get(
            "charging_rules", []
        )

        return len(rules)

    @property
    def extra_state_attributes(self):
        return {
            "rules": self.coordinator.data.get(
                "charging_rules",
                [],
            )
        }