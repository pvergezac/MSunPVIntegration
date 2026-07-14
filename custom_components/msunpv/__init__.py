"""
Custom integration to integrate MSunPV solar router  with Home Assistant.

For more details about this integration, please refer to
https://github.com/pvergezac/MSunPVIntegration

For more details about MSunPV : https://ard-tek.com/index.php
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform

from .const import DOMAIN, LOGGER
from .coordinator import MSunPVDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up MSunPV integration using UI."""
    LOGGER.debug(
        "Setting up MSunPV integration - entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    coordinator = MSunPVDataUpdateCoordinator(hass=hass, config_entry=entry)

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Propage le configEntry à toutes les plateformes déclarées dans l'intégration.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Subscrib to unload event
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    LOGGER.info("MSunPV Integration successfully initialized")

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
