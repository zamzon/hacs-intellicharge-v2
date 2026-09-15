"""API client for IntelliCharge."""

import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)

API_BASE_URL = "https://api.intellicharge.ai"
API_LOGIN_URL = f"{API_BASE_URL}/api/v1/login/access-token"


class IntelliChargeAPI:
    """IntelliCharge API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
        inverter_id: str,
    ) -> None:
        self._session = session
        self._username = username
        self._password = password

        # Vi bruger plant_id her
        self._plant_id = inverter_id

        self._access_token = None

    async def _get_access_token(self) -> str:
        """Login and get token."""

        data = {
            "username": self._username,
            "password": self._password,
        }

        async with self._session.post(
            API_LOGIN_URL,
            data=data,
        ) as response:
            response.raise_for_status()

            result = await response.json()

            self._access_token = result["access_token"]

            return self._access_token

    async def _headers(self) -> dict:
        """Return auth headers."""

        if not self._access_token:
            await self._get_access_token()

        return {
            "Authorization": f"Bearer {self._access_token}"
        }

    async def async_test_connection(self):
        """Validate credentials."""

        headers = await self._headers()

        url = (
            f"{API_BASE_URL}/api/v2/plants/"
            f"{self._plant_id}"
        )

        async with self._session.get(
            url,
            headers=headers,
        ) as response:
            response.raise_for_status()

            return await response.json()

    async def async_get_data(self):
        """Compatibility method for coordinator."""

        headers = await self._headers()

        url = (
            f"{API_BASE_URL}/api/v2/plants/"
            f"{self._plant_id}/settings/"
        )

        async with self._session.get(
            url,
            headers=headers,
        ) as response:
            response.raise_for_status()

            return await response.json()

    async def async_get_custom_charging_rules(self):
        """Get charging rules."""

        headers = await self._headers()

        url = (
            f"{API_BASE_URL}/api/v2/plants/"
            f"{self._plant_id}/pvms-ems/custom-charging-rules/"
        )

        async with self._session.get(
            url,
            headers=headers,
        ) as response:
            response.raise_for_status()

            return await response.json()

    async def async_set_custom_charging_rules(self, rules):
        """Set charging rules."""

        headers = await self._headers()

        headers["Content-Type"] = "application/json"

        url = (
            f"{API_BASE_URL}/api/v2/plants/"
            f"{self._plant_id}/pvms-ems/custom-charging-rules/"
        )

        async with self._session.post(
            url,
            json=rules,
            headers=headers,
        ) as response:
            response.raise_for_status()

            return True

    async def async_set_min_soc_after_sell(
        self,
        value: int,
    ):
        """Set minimum battery SOC after sell."""

        rules = [
            {
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
        ]

        return await self.async_set_custom_charging_rules(
            rules
        )