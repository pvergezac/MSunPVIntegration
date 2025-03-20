"""
Custom integration to integrate MSunPV solar router  with Home Assistant.

For more details about this integration, please refer to
https://github.com/pvergezac/MSunPVIntegration

For more details about MSunPV : https://ard-tek.com/index.php
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_HOST, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import MsunPVApiClient
from .const import CONF_MSUNPV_TYPE, CONF_SONDES_COMP, DOMAIN, LOGGER
from .coordinator import MSunPVDataUpdateCoordinator
from .data import MsunPVData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MsunPVConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: MsunPVConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    LOGGER.debug(
        "Appel de <<__init__>> async_setup_entry entry: entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    coordinator = MSunPVDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=1),
    )

    with_sonde_comp: bool = str(entry.data[CONF_SONDES_COMP]) == "True"

    entry.runtime_data = MsunPVData(
        client=MsunPVApiClient(
            url=entry.data[CONF_HOST],
            router_type=entry.data[CONF_MSUNPV_TYPE],
            sondes_comp=with_sonde_comp,
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    # propage le configEntry à toutes les plateformes déclarées dans l'intégration.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Subscrib to unload event
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MsunPVConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: MsunPVConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
