"""Switch platform for msunpv."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from custom_components.msunpv.const import DOMAIN

from .entity import MsunPVEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MSunPVDataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="msunpv",
        name="MSunPV Demo Switch",
        icon="mdi:format-quote-close",
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
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        # return self.coordinator.data.get("title", "") == "foo"  # noqa: ERA001
        return False

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        # await self.coordinator.client.async_set_title("bar")  # noqa: ERA001
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        # await self.coordinator.client.async_set_title("foo")  # noqa: ERA001
        await self.coordinator.async_request_refresh()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch (sync wrapper)."""
        # asyncio.create_task(self.async_turn_on(**kwargs))  # noqa: ERA001

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch (sync wrapper)."""
        # asyncio.create_task(self.async_turn_off(**kwargs))  # noqa: ERA001
