"""Sensor platform for msunpv."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature

from .const import CONF_MSUNPV_TYPE, CONF_SONDES_COMP, LOGGER, MSPV_2_2d, MSPV_4_4d
from .entity import MsunPVEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MSunPVDataUpdateCoordinator
    from .data import MsunPVConfigEntry


ENTITY_DESCRIPTIONS_SPECIFIQUE_MSPV_2_2d = (
    SensorEntityDescription(
        key="outbal",
        name="Ratio routage Ballon",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="%",
        icon="mdi:percent",
    ),
    SensorEntityDescription(
        key="outrad",
        name="Ratio routage Radiateur",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="%",
        icon="mdi:percent",
    ),
)

ENTITY_DESCRIPTIONS_SPECIFIQUE_MSPV_4_4d = (
    SensorEntityDescription(
        key="outbal",
        name="Puissance routage Ballon",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="outrad",
        name="Puissance routage Radiateur",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="conso_ballon_jour",
        name="Energie cumulus journalière",
        icon="mdi:water-boiler",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="conso_radiateur_jour",
        name="Energie radiateur journalière",
        icon="mdi:radiator",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
)

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="powreso",
        name="Puissance Réseau",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="powpv",
        name="Puissance Solaire",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="tbal",
        name="Température Ballon",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="tsdb",
        name="Température SdB",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="tamb",
        name="Température ambiante",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="consommation_jour",
        name="Energie Import Réseau",
        icon="mdi:transmission-tower-import",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="injection_jour",
        name="Energie Export Réseau",
        icon="mdi:transmission-tower-export",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="production_jour",
        name="Energie Production Solaire",
        icon="mdi:counter",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="production_cumul",
        name="Energie Production Solaire (cumul)",
        icon="mdi:counter",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=0,
    ),
    # Valeurs calculées
    SensorEntityDescription(
        key="production_jour_cons",
        name="Energie Production Solaire Consommée",
        icon="mdi:solar-power",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="consommation_globale",
        name="Energie Consommation globale",
        icon="mdi:solar-power",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="powpv_inj",
        name="Puissance Solaire injectée",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="powpv_cons",
        name="Puissance Solaire consomée",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
    ),
    # Infos routeur
    SensorEntityDescription(
        key="rssi",
        name="Wifi signal",
        icon="mdi:wifi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dB",
    ),
    SensorEntityDescription(
        key="modele",
        name="Modele du routeur",
    ),
    SensorEntityDescription(
        key="version",
        name="Version du projet",
    ),
    SensorEntityDescription(
        key="sernum",
        name="Numéro de série",
    ),
    SensorEntityDescription(
        key="fwrout",
        name="Firmware routeur",
    ),
    SensorEntityDescription(
        key="fwwifi",
        name="Firmware Wifi",
    ),
)

ENTITY_DESCRIPTIONS_COMP = (
    SensorEntityDescription(
        key="sonde_8",
        name="Sonde08",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_9",
        name="Sonde09",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_10",
        name="Sonde10",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_11",
        name="Sonde11",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_12",
        name="Sonde12",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_13",
        name="Sonde13",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_14",
        name="Sonde14",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sonde_15",
        name="Sonde15",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MsunPVConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    type_router: str = entry.data[CONF_MSUNPV_TYPE]
    with_sonde_comp: bool = str(entry.data[CONF_SONDES_COMP]) == "True"

    LOGGER.debug(
        "Appel <sensor> async_setup_entry : entry_id='%s', data='%s', router_type='%s', sonde_comp='%r'",  # noqa: E501
        entry.entry_id,
        entry.data,
        type_router,
        with_sonde_comp,
        # entry.runtime_data.router_type,
        # entry.runtime_data.sondes_comp,
    )

    list_ent = ENTITY_DESCRIPTIONS

    if type_router == MSPV_4_4d:
        LOGGER.debug("Pour mspv 4x4")
        list_ent += ENTITY_DESCRIPTIONS_SPECIFIQUE_MSPV_4_4d
    elif type_router == MSPV_2_2d:
        LOGGER.debug("Pour mspv 2x2")
        list_ent += ENTITY_DESCRIPTIONS_SPECIFIQUE_MSPV_2_2d

    ##if str(entry.data[CONF_SONDES_COMP]) == "True":
    if with_sonde_comp:
        LOGGER.debug("Avec sondes complementaires")
        list_ent += ENTITY_DESCRIPTIONS_COMP

    async_add_entities(
        MsunPVSensor(
            entry_id=entry.entry_id,
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in list_ent
    )


class MsunPVSensor(MsunPVEntity, SensorEntity):
    """msunpv Sensor class."""

    def __init__(
        self,
        entry_id: str,
        coordinator: MSunPVDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.entity_id = f"{SENSOR_DOMAIN}.{entity_description.key}"
        self._attr_unique_id = f"{entry_id}_{entity_description.key}"
        self.msparam = entity_description.key

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self.entity_description.key)

        return None

    @property
    def extra_state_attributes(self) -> Any | None:
        """Return the state attributes of the sensor."""
        # Retourne l'heure transmise apr le routeur
        if self.coordinator.data:
            return {"last_update": self.coordinator.data.get("time")}

        return None
