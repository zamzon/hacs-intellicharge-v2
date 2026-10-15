"""Sensor platform for IntelliCharge."""

import logging

from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)
_LOGGER.error("INTELLICHARGE TEST SENSOR LOADED")


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    _LOGGER.error("INTELLICHARGE async_setup_entry CALLED")

    async_add_entities(
        [
            IntelliChargeTestSensor(),
        ]
    )


class IntelliChargeTestSensor(SensorEntity):
    _attr_name = "IntelliCharge Test"
    _attr_unique_id = "intellicharge_test"

    @property
    def native_value(self):
        return "OK"
