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
            IntelliChargeCurrentActionDescriptionSensor(
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

        self._attr_name = "IntelliCharge Charging Rules"
        self._attr_unique_id = (
            "intellicharge_charging_rules"
        )

        self._attr_entity_registry_enabled_default = (
            False
        )

    @property
    def native_value(self):
        return len(
            self.coordinator.data.get(
                "charging_rules",
                [],
            )
        )


class IntelliChargeCurrentActionSensor(
    CoordinatorEntity,
    SensorEntity,
):
    ACTION_NAMES = {
        "self_consumption": "Eget forbrug",
        "charge": "Opladning",
        "discharge": "Afladning",
        "idle": "Standby",
        "locked": "Låst",
        "no_new_command": "Ingen ny kommando",
    }

    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = (
            "IntelliCharge Current Action"
        )

        self._attr_unique_id = (
            "intellicharge_current_action"
        )

        self._attr_icon = (
            "mdi:battery-charging"
        )

    @property
    def native_value(self):
        data = (
            self.coordinator.data.get(
                "current_action",
                {},
            )
            or {}
        )

        mode = data.get("charge_mode")

        return self.ACTION_NAMES.get(
            mode,
            mode or "Ukendt",
        )


class IntelliChargeCurrentActionDescriptionSensor(
    CoordinatorEntity,
    SensorEntity,
):
    DESCRIPTIONS = {
        "self_consumption":
            "Systemet bruger den genererede energi til dit forbrug, opbevarer overskuddet i batteriet og sender overskydende energi til elnettet, når batteriet er fuldt. Hvis det er nødvendigt, importeres ekstra energi fra elnettet.",

        "charge":
            "Systemet oplader batteriet fra elnettet enten for at dække forventede energibehov eller for at lagre energi til fremtidigt salg og fortjeneste.",

        "discharge":
            "Systemet aflader batteriet til elnettet og sælger den lagrede energi for ekstra indtægter.",

        "idle":
            "Systemet er på standby og bevarer den lagrede energi til senere brug, når priserne er højere. Nuværende energibehov dækkes af produceret energi eller importeres fra elnettet.",

        "locked":
            "Systemet er låst, og batteriet er ikke i brug. Forbruget dækkes af solenergi (eller importeres om nødvendigt), og overskuddet sendes til elnettet.",

        "no_new_command":
            "Ingen ny kommando blev sendt denne time; systemet er enten i selvforbrugstilstand eller følger den sidste kommando.",
    }

    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = (
            "IntelliCharge Current Action Description"
        )

        self._attr_unique_id = (
            "intellicharge_current_action_description"
        )

        self._attr_icon = "mdi:text"

    @property
    def native_value(self):
        data = (
            self.coordinator.data.get(
                "current_action",
                {},
            )
            or {}
        )

        mode = data.get("charge_mode")

        return self.DESCRIPTIONS.get(
            mode,
            "Ukendt",
        )
