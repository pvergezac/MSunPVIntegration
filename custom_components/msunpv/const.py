"""Constants for MSunPV."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "msunpv"
ATTRIBUTION = "MSunPV(local) from Ard-Tek (https://ard-tek.com/)"

CONF_MSUNPV_MODELE = "msunpv_modele"
CONF_MSUNPV_TYPE = "msunpv_type"
MSPV_2_2D = "mspv2_2d"
MSPV_4_4D = "mspv4_4d"
CONF_MSUNPV_TYPES = [MSPV_2_2D, MSPV_4_4D]
CONF_SONDES_COMP = "sondes_comp"

# Update interval
UPDATE_INTERVAL_SECONDS = 60

# Storage key for persistence
STORAGE_KEY = f"{DOMAIN}_data"
STORAGE_VERSION = 1

# decod_option
DECOD_OPTION_RTCC: int = 0x00000001
DECOD_OPTION_PARAMSYS = 0x00000002
DECOD_OPTION_INANS = 0x00000004
DECOD_OPTION_SURVMM = 0x00000008
DECOD_OPTION_CMDPOS = 0x00000010
DECOD_OPTION_OUTSTAT = 0x00000020
DECOD_OPTION_CPTVALS = 0x00000040
DECOD_OPTION_CHOUTVAL = 0x00000080

DECOD_OPTION_ALL: int = (
    DECOD_OPTION_RTCC
    | DECOD_OPTION_PARAMSYS
    | DECOD_OPTION_INANS
    | DECOD_OPTION_SURVMM
    | DECOD_OPTION_CMDPOS
    | DECOD_OPTION_OUTSTAT
    | DECOD_OPTION_CPTVALS
    | DECOD_OPTION_CHOUTVAL
)

DECOD_OPTION_STD: int = (
    DECOD_OPTION_RTCC
    | DECOD_OPTION_PARAMSYS
    | DECOD_OPTION_INANS
    # | DECOD_OPTION_SURVMM
    | DECOD_OPTION_CMDPOS
    | DECOD_OPTION_OUTSTAT
    | DECOD_OPTION_CPTVALS
    | DECOD_OPTION_CHOUTVAL
)

CMD_MANU_BAL: list[int] = [0, 0b11111100, 0b00000001]
CMD_AUTO_BAL: list[int] = [0, 0b11111100, 0b00000010]
CMD_MANU_RAD: list[int] = [0, 0b11110011, 0b00000100]
CMD_AUTO_RAD: list[int] = [0, 0b11110011, 0b00001000]

CMD_TEST_ROUTEUR_INJECTION: list[int] = [7, 0b11110000, 0b00000001]
CMD_TEST_ROUTEUR_ZERO: list[int] = [7, 0b11110000, 0b00000010]
CMD_TEST_ROUTEUR_MOYEN: list[int] = [7, 0b11110000, 0b00000100]
CMD_TEST_ROUTEUR_FORT: list[int] = [7, 0b11110000, 0b00001000]

# les données du MSunPV
## Les mesures et sondes
MSPV_POWRESO = "powreso"
MSPV_POWPV = "powpv"
MSPV_OUTBAL = "outbal"
MSPV_OUTRAD = "outrad"
MSPV_TBAL = "tbal"
MSPV_TSDB = "tsdb"
MSPV_TAMB = "tamb"
MSPV_POWPV_INJ = "powpv_inj"
MSPV_POWPV_CONS = "powpv_cons"
##Les cumuls journaliers et globaux
MSPV_CONSOMMATION_JOUR = "consommation_jour"
MSPV_INJECTION_JOUR = "injection_jour"
MSPV_PRODUCTION_JOUR = "production_jour"
MSPV_PRODUCTION_JOUR_CONS = "production_jour_cons"
MSPV_CONSOMMATION_GLOBALE = "consommation_globale"
MSPV_CONSOMMATION_BALLON_JOUR = "conso_ballon_jour"
MSPV_CONSOMMATION_RADIATEUR_JOUR = "conso_radiateur_jour"
MSPV_CONSOMMATION_RESEAU_CUMUL = "consommation_reseau_cumul"
MSPV_INJECTION_RESEAU_CUMUL = "injection_reseau_cumul"
MSPV_PRODUCTION_CUMUL = "production_cumul"
## Les param sys
MSPV_DATE = "date"
MSPV_TIME = "time"
MSPV_MODELE = "modele"
MSPV_VERSION = "version"
MSPV_SERNUM = "sernum"
MSPV_FWROUT = "fwrout"
MSPV_FWWIFI = "fwwifi"
## Les surveillances de mesures
MSPV_SURVMM = "survmm"
## Les commandes
MSPV_CMDPOS = "cmdpos"
MSPV_MANUBAL = "manubal"
MSPV_AUTOBAL = "autobal"
MSPV_MANURAD = "manurad"
MSPV_AUTORAD = "autorad"
MSPV_TEST_ROUTEUR = "test_routeur"
##Les etats des sorties
MSPV_OUTSTATS = "outstats"
## Les valeurs calculées en sortie des modules chauffage
MSPV_CHOUTVALS = "choutvals"
MSPV_SONDE_9 = "sonde_9"
MSPV_SONDE_10 = "sonde_10"
MSPV_SONDE_11 = "sonde_11"
MSPV_SONDE_12 = "sonde_12"
MSPV_SONDE_13 = "sonde_13"
MSPV_SONDE_14 = "sonde_14"
MSPV_SONDE_15 = "sonde_15"
MSPV_SONDE_16 = "sonde_16"
MSPV_RSSI = "rssi"

MSPV_INJECT = "inject"
MSPV_ZERO = "zero"
MSPV_MOYEN = "moyen"
MSPV_FORT = "fort"

MSPV_TEST_ROUTEUR_OPTIONS: dict[int, str] = {
    1: MSPV_INJECT,
    2: MSPV_ZERO,
    4: MSPV_MOYEN,
    8: MSPV_FORT,
}
