"""DataUpdateCoordinator for msunpv."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import (
    MsunPVApiClient,
    MsunPVApiClientAuthenticationError,
    MsunPVApiClientError,
    MSunPVApiData,
)
from .const import (
    CONF_MSUNPV_TYPE,
    CONF_SONDES_COMP,
    DOMAIN,
    STORAGE_KEY,
    STORAGE_VERSION,
    UPDATE_INTERVAL_SECONDS,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class MSunPVDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize MSunPVDataUpdateCoordinator."""
        self.config_entry = config_entry
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.stored_data: None | dict[str, Any] = None
        with_sonde_comp: bool = str(config_entry.data[CONF_SONDES_COMP]) == "True"

        self.client = MsunPVApiClient(
            url=config_entry.data[CONF_HOST],
            router_type=config_entry.data[CONF_MSUNPV_TYPE],
            sondes_comp=with_sonde_comp,
            session=async_get_clientsession(hass),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            data: MSunPVApiData = await self.client.async_get_data()
        except MsunPVApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except MsunPVApiClientError as exception:
            raise UpdateFailed(exception) from exception
        else:
            # Gestion des cumuls
            self.stored_data = await self.async_load_state()

            delta = data.consommation_jour - self.stored_data["consommation_jour"]
            delta = max(delta, 0)
            self.stored_data["consommation_jour"] = data.consommation_jour
            self.stored_data["consommation_reseau_cumul"] += delta
            data.consommation_reseau_cumul = self.stored_data[
                "consommation_reseau_cumul"
            ]

            delta = data.injection_jour - self.stored_data["injection_jour"]
            delta = max(delta, 0)
            self.stored_data["injection_jour"] = data.injection_jour
            self.stored_data["injection_reseau_cumul"] += delta
            data.injection_reseau_cumul = self.stored_data["injection_reseau_cumul"]

            await self._save_state()

            return data

    async def _save_state(self) -> None:
        """Persist runtime data across HA restarts."""
        _LOGGER.debug("Saving state: %s", self.stored_data)
        await self._store.async_save(self.stored_data)

    async def async_load_state(self) -> dict[str, Any]:
        """Load persisted state on startup."""
        stored: None | dict[str, Any]
        # if not self.stored_data or not self.stored_data["last_reset_date"]:
        stored = await self._store.async_load()

        if (not stored) or (stored is None) or (stored["last_reset_date"] is None):
            stored = {
                "last_reset_date": dt_util.now().date().isoformat(),
                "consommation_jour": 0,
                "consommation_reseau_cumul": 0,
                "injection_jour": 0,
                "injection_reseau_cumul": 0,
            }

        today = dt_util.now().date()
        stored_date_str = stored.get("last_reset_date")
        try:
            stored_date = (
                date.fromisoformat(stored_date_str) if stored_date_str else None
            )
        except (ValueError, TypeError):
            stored_date = None

        if stored_date == today:
            _LOGGER.info("Restored today's runtime: ")
        else:
            _LOGGER.info("New day detected -- resetting daily counters")

        return stored
