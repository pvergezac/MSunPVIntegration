"""DataUpdateCoordinator for msunpv."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    MsunPVApiClientAuthenticationError,
    MsunPVApiClientError,
)

if TYPE_CHECKING:
    from .data import MsunPVConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class MSunPVDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: MsunPVConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except MsunPVApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except MsunPVApiClientError as exception:
            raise UpdateFailed(exception) from exception
