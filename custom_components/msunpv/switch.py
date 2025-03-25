"""Switch platform for msunpv."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import MsunPVEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MSunPVDataUpdateCoordinator
    from .data import MsunPVConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="msunpv",
        name="MSunPV Demo Switch",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MsunPVConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        MsunPVSwitch(
            coordinator=entry.runtime_data.coordinator,
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
        # await self.coordinator.config_entry.runtime_data.client.async_set_title("bar")  # noqa: ERA001
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        # await self.coordinator.config_entry.runtime_data.client.async_set_title("foo")  # noqa: ERA001
        await self.coordinator.async_request_refresh()
