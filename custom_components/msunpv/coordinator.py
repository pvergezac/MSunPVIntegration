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
)
from .const import (
    CONF_MSUNPV_TYPE,
    CONF_SONDES_COMP,
    DOMAIN,
    MSPV_CONSOMMATION_JOUR,
    MSPV_CONSOMMATION_RESEAU_CUMUL,
    MSPV_FORT,
    MSPV_INJECT,
    MSPV_INJECTION_JOUR,
    MSPV_INJECTION_RESEAU_CUMUL,
    MSPV_MOYEN,
    MSPV_ZERO,
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
        self.hass = hass
        self.config_entry = config_entry
        self.url = config_entry.data[CONF_HOST]
        self.name = DOMAIN
        self.router_type = config_entry.data[CONF_MSUNPV_TYPE]
        self.with_sonde_comp: bool = str(config_entry.data[CONF_SONDES_COMP]) == "True"

        self._store: Store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.stored_data: None | dict[str, Any] = None

        self.client = MsunPVApiClient(
            url=self.url,
            router_type=self.router_type,
            sondes_comp=self.with_sonde_comp,
            session=async_get_clientsession(hass),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        try:
            # Lecture de status.xml du routeur
            self.data = await self.client.async_get_status_xml_data()
        except MsunPVApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except MsunPVApiClientError as exception:
            raise UpdateFailed(exception) from exception
        else:
            # Gestion des cumuls
            self.stored_data = await self.async_load_state()

            delta = (
                self.data[MSPV_CONSOMMATION_JOUR]
                - self.stored_data[MSPV_CONSOMMATION_JOUR]
            )
            delta = max(delta, 0)
            self.stored_data[MSPV_CONSOMMATION_JOUR] = self.data[MSPV_CONSOMMATION_JOUR]
            self.stored_data[MSPV_CONSOMMATION_RESEAU_CUMUL] += delta
            self.data[MSPV_CONSOMMATION_RESEAU_CUMUL] = self.stored_data[
                MSPV_CONSOMMATION_RESEAU_CUMUL
            ]

            delta = (
                self.data[MSPV_INJECTION_JOUR] - self.stored_data[MSPV_INJECTION_JOUR]
            )
            delta = max(delta, 0)
            self.stored_data[MSPV_INJECTION_JOUR] = self.data[MSPV_INJECTION_JOUR]
            self.stored_data[MSPV_INJECTION_RESEAU_CUMUL] += delta
            self.data[MSPV_INJECTION_RESEAU_CUMUL] = self.stored_data[
                MSPV_INJECTION_RESEAU_CUMUL
            ]

            # Mémorise les cumuls
            await self._save_state()

            return self.data

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
                MSPV_CONSOMMATION_JOUR: 0,
                MSPV_CONSOMMATION_RESEAU_CUMUL: 0,
                MSPV_INJECTION_JOUR: 0,
                MSPV_INJECTION_RESEAU_CUMUL: 0,
            }

        today = dt_util.now().date()
        stored_date_str: str | None = stored.get("last_reset_date")

        try:
            stored_date = (
                date.fromisoformat(stored_date_str) if stored_date_str else None
            )
        except (ValueError, TypeError):
            stored_date = None

        if stored_date != today:
            _LOGGER.info("New day detected -- resetting daily counters")
            stored = {
                "last_reset_date": dt_util.now().date().isoformat(),
                MSPV_CONSOMMATION_JOUR: 0,
                MSPV_CONSOMMATION_RESEAU_CUMUL: 0,
                MSPV_INJECTION_JOUR: 0,
                MSPV_INJECTION_RESEAU_CUMUL: 0,
            }

        return stored

    async def async_set_manu_bal_on(self) -> None:
        """Set the manual ballon switch on."""
        _LOGGER.debug("set_manu_bal_on")
        await self.client.async_set_manu_bal_on()
        await self.async_request_refresh()

    async def async_set_manu_bal_off(self) -> None:
        """Set the manual ballon switch off."""
        _LOGGER.debug("set_manu_bal_off")
        await self.client.async_set_manu_bal_off()
        await self.async_request_refresh()

    async def async_set_auto_bal_on(self) -> None:
        """Set the auto ballon switch on."""
        _LOGGER.debug("set_auto_bal_on")
        await self.client.async_set_auto_bal_on()
        await self.async_request_refresh()

    async def async_set_auto_bal_off(self) -> None:
        """Set the auto ballon switch off."""
        _LOGGER.debug("set_auto_bal_off")
        await self.client.async_set_auto_bal_off()
        await self.async_request_refresh()

    async def async_set_manu_rad_on(self) -> None:
        """Set the manual radiateur switch on."""
        await self.client.async_set_manu_rad_on()
        await self.async_request_refresh()

    async def async_set_manu_rad_off(self) -> None:
        """Set the manual radiateur switch off."""
        await self.client.async_set_manu_rad_off()
        await self.async_request_refresh()

    async def async_set_auto_rad_on(self) -> None:
        """Set the manual radiateur switch on."""
        await self.client.async_set_auto_rad_on()
        await self.async_request_refresh()

    async def async_set_auto_rad_off(self) -> None:
        """Set the manual radiateur switch off."""
        await self.client.async_set_auto_rad_off()
        await self.async_request_refresh()

    async def async_set_test_routeur(self, value: str) -> None:
        """Set the test router command."""
        _LOGGER.debug("set_test_routeur: %s", value)
        if value == MSPV_INJECT:
            await self.client.async_set_test_routeur_inject()
        elif value == MSPV_ZERO:
            await self.client.async_set_test_routeur_zero()
        elif value == MSPV_MOYEN:
            await self.client.async_set_test_routeur_moyen()
        elif value == MSPV_FORT:
            await self.client.async_set_test_routeur_fort()
        else:
            msg = f"async_set_test_routeur - valeurs incorrect: {value}"
            raise ValueError(msg)

        await self.async_request_refresh()
