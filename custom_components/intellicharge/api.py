"""Sensor platform for IntelliCharge."""

from homeassistant.components.sensor import SensorEntity

DOMAIN = "intellicharge"


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    async_add_entities(
        [
            IntelliChargeTestSensor(),
        ]
    )


class IntelliChargeTestSensor(SensorEntity):
    def __init__(self):
        self._attr_name = "IntelliCharge Test"
        self._attr_unique_id = "intellicharge_test"

    @property
    def native_value(self):
        return "OK"
