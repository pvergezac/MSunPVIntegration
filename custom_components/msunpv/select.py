"""Select platform for msunpv."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.select import SelectEntity, SelectEntityDescription

from custom_components.msunpv.const import (
    DOMAIN,
    MSPV_FORT,
    MSPV_INJECT,
    MSPV_MOYEN,
    MSPV_TEST_ROUTEUR,
    MSPV_ZERO,
)
from custom_components.msunpv.entity import MsunPVEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MSunPVDataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SelectEntityDescription(
        key=MSPV_TEST_ROUTEUR,
        icon="mdi:target",
        options=[MSPV_INJECT, MSPV_ZERO, MSPV_MOYEN, MSPV_FORT],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator: MSunPVDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        MsunPVSelect(coordinator=coordinator, entity_description=entity_description)
        for entity_description in ENTITY_DESCRIPTIONS
    )


class MsunPVSelect(MsunPVEntity, SelectEntity):
    """msunpv select class."""

    _attr_has_entity_name = True
    _attr_translation_key = MSPV_TEST_ROUTEUR

    def __init__(
        self,
        coordinator: MSunPVDataUpdateCoordinator,
        entity_description: SelectEntityDescription,
    ) -> None:
        """Initialize the select class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def current_option(self) -> str:
        """Return the current option."""
        data = self.coordinator.data or {}
        return data.get(self.entity_description.key) or "unknown"

    async def async_select_option(self, option: str) -> None:
        """Change mode when user selects from dropdown."""
        self._attr_current_option = option
        await self.coordinator.async_set_test_routeur(option)

    def select_option(self, option: str) -> None:
        """Select option."""
        raise NotImplementedError
