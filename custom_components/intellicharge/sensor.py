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
            ),
            IntelliChargeCurrentActionSensor(
                coordinator
            ),
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


class IntelliChargeCurrentActionSensor(
    CoordinatorEntity,
    SensorEntity,
):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = (
            "IntelliCharge Current Action"
        )

        self._attr_unique_id = (
            "intellicharge_current_action"
        )

    @property
    def native_value(self):
        data = self.coordinator.data.get(
            "current_action",
            {},
        )

        return (
            data.get("action")
            or data.get("status")
            or data.get("title")
            or data.get("current_action")
            or "Unknown"
        )

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get(
            "current_action",
            {},
        )
