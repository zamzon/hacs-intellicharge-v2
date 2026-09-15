"""Config flow for IntelliCharge."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import IntelliChargeAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "intellicharge"
CONF_INVERTER_ID = "inverter_id"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_INVERTER_ID): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle IntelliCharge config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the user step."""

        errors: dict[str, str] = {}

        if user_input is not None:

            session = async_get_clientsession(self.hass)

            api = IntelliChargeAPI(
                session=session,
                username=user_input[CONF_USERNAME],
                password=user_input[CONF_PASSWORD],
                inverter_id=user_input[CONF_INVERTER_ID],
            )

            try:
                await api.async_test_connection()

            except Exception as err:
                _LOGGER.exception(
                    "Error validating IntelliCharge connection: %s",
                    err,
                )
                errors["base"] = "cannot_connect"

            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_USERNAME]}_{user_input[CONF_INVERTER_ID]}"
                )

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=(
                        f"IntelliCharge "
                        f"({user_input[CONF_INVERTER_ID]})"
                    ),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )