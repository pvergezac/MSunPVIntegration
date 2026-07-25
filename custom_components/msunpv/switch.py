"""Switch platform for msunpv."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from custom_components.msunpv.const import (
    DOMAIN,
    MSPV_AUTOBAL,
    MSPV_AUTORAD,
    MSPV_MANUBAL,
    MSPV_MANURAD,
)
from custom_components.msunpv.entity import MsunPVEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MSunPVDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key=MSPV_MANUBAL,
        icon="mdi:hand-back-left-outline",
        translation_key=MSPV_MANUBAL,
        has_entity_name=True,
    ),
    SwitchEntityDescription(
        key=MSPV_AUTOBAL,
        icon="mdi:calendar-clock",
        translation_key=MSPV_AUTOBAL,
        has_entity_name=True,
    ),
    SwitchEntityDescription(
        key=MSPV_MANURAD,
        icon="mdi:hand-back-left-outline",
        translation_key=MSPV_MANURAD,
        has_entity_name=True,
    ),
    SwitchEntityDescription(
        key=MSPV_AUTORAD,
        icon="mdi:calendar-clock",
        translation_key=MSPV_AUTORAD,
        has_entity_name=True,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    coordinator: MSunPVDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MsunPVSwitch(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class MsunPVSwitch(MsunPVEntity, SwitchEntity):
    """msunpv switch class."""

    def __init__(
        self,
        coordinator: MSunPVDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the switch."""
        return f"{self.entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        # return self.coordinator.data.get("title", "") == "foo"  # noqa: ERA001
        data = self.coordinator.data or {}
        key = self.entity_description.key
        return data.get(key, False)

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        _LOGGER.debug("Turn on : %s", self.entity_description.key)
        if self.entity_description.key == MSPV_MANUBAL:
            await self.coordinator.async_set_manu_bal_on()
        elif self.entity_description.key == MSPV_AUTOBAL:
            await self.coordinator.async_set_auto_bal_on()
        elif self.entity_description.key == MSPV_MANURAD:
            await self.coordinator.async_set_manu_rad_on()
        elif self.entity_description.key == MSPV_AUTORAD:
            await self.coordinator.async_set_auto_rad_on()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        if self.entity_description.key == MSPV_MANUBAL:
            await self.coordinator.async_set_manu_bal_off()
        elif self.entity_description.key == MSPV_AUTOBAL:
            await self.coordinator.async_set_auto_bal_off()
        elif self.entity_description.key == MSPV_MANURAD:
            await self.coordinator.async_set_manu_rad_off()
        elif self.entity_description.key == MSPV_AUTORAD:
            await self.coordinator.async_set_auto_rad_off()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch (sync wrapper)."""
        # asyncio.create_task(self.async_turn_on(**kwargs))     # noqa: ERA001
        # asyncio.run(self.async_turn_on(**kwargs))    # noqa: ERA001
        raise NotImplementedError

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch (sync wrapper)."""
        # asyncio.create_task(self.async_turn_off(**kwargs))    # noqa: ERA001
        # asyncio.run(self.async_turn_off(**kwargs))    # noqa: ERA001
        raise NotImplementedError
