"""Adds config flow for MSunPV."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    MsunPVApiClient,
    MsunPVApiClientAuthenticationError,
    MsunPVApiClientCommunicationError,
    MsunPVApiClientError,
)
from .const import (
    CONF_MSUNPV_TYPE,
    CONF_MSUNPV_TYPES,
    CONF_SONDES_COMP,
    DOMAIN,
    LOGGER,
    MSPV_2_2d,
)


class MSunPVFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for MsunPV."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_api(
                    url=user_input[CONF_HOST],
                    router_type=user_input[CONF_MSUNPV_TYPE],
                    sondes_comp=str(user_input[CONF_SONDES_COMP]) == "True",
                )
            except MsunPVApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except MsunPVApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except MsunPVApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_HOST])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default="http://"): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        )
                    ),
                    vol.Required(
                        CONF_MSUNPV_TYPE, default=MSPV_2_2d
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=CONF_MSUNPV_TYPES,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Required("nom", default="MsunPV-1"): selector.TextSelector(
                        selector.TextSelectorConfig()
                    ),
                    vol.Required(CONF_SONDES_COMP): selector.BooleanSelector(
                        selector.BooleanSelectorConfig()
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_api(self, url: str, router_type: str, sondes_comp: bool) -> None:  # noqa: FBT001
        """Validate api url."""
        client = MsunPVApiClient(
            url=url,
            router_type=router_type,
            sondes_comp=sondes_comp,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
