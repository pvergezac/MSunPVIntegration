"""Constants for MSunPV."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "msunpv"
ATTRIBUTION = "MSunPV(local) from Ard-Tek (https://ard-tek.com/)"

CONF_MSUNPV_MODELE = "msunpv_modele"

MSPV_2_2d = "MS_PV2_2d"
MSPV_4_4d = "MS_PV4_4d"

CONF_MSUNPV_TYPE = "msunpv_type"
CONF_MSUNPV_TYPES = [MSPV_2_2d, MSPV_4_4d]


CONF_SONDES_COMP = "sondes_comp"
