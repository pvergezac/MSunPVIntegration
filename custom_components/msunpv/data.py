"""Custom types for msunpv."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import MsunPVApiClient
    from .coordinator import MSunPVDataUpdateCoordinator


type MsunPVConfigEntry = ConfigEntry[MsunPVData]


@dataclass
class MsunPVData:
    """Data for the MSunPV integration."""

    client: MsunPVApiClient
    coordinator: MSunPVDataUpdateCoordinator
    integration: Integration
