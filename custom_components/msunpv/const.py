"""Constants for MSunPV."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "msunpv"
ATTRIBUTION = "MSunPV(local) from Ard-Tek (https://ard-tek.com/)"

CONF_MSUNPV_MODELE = "msunpv_modele"

MSPV_2_2D = "mspv2_2d"
MSPV_4_4D = "mspv4_4d"

CONF_MSUNPV_TYPE = "msunpv_type"
CONF_MSUNPV_TYPES = [MSPV_2_2D, MSPV_4_4D]


CONF_SONDES_COMP = "sondes_comp"

# Update interval
UPDATE_INTERVAL_SECONDS = 60


# Storage key for persistence
STORAGE_KEY = f"{DOMAIN}_data"
STORAGE_VERSION = 1
