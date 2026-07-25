"""Sample API Client."""

from __future__ import annotations

import logging
import socket
from typing import Any

import aiohttp
import async_timeout
import xmltodict

from .const import (
    CMD_AUTO_BAL,
    CMD_AUTO_RAD,
    CMD_MANU_BAL,
    CMD_MANU_RAD,
    CMD_TEST_ROUTEUR_FORT,
    CMD_TEST_ROUTEUR_INJECTION,
    CMD_TEST_ROUTEUR_MOYEN,
    CMD_TEST_ROUTEUR_ZERO,
    DECOD_OPTION_ALL,
    DECOD_OPTION_CMDPOS,
    DECOD_OPTION_CPTVALS,
    DECOD_OPTION_INANS,
    DECOD_OPTION_PARAMSYS,
    MSPV_2_2D,
    MSPV_4_4D,
    MSPV_AUTOBAL,
    MSPV_AUTORAD,
    MSPV_CHOUTVALS,
    MSPV_CONSOMMATION_BALLON_JOUR,
    MSPV_CONSOMMATION_GLOBALE,
    MSPV_CONSOMMATION_JOUR,
    MSPV_CONSOMMATION_RADIATEUR_JOUR,
    MSPV_DATE,
    MSPV_FWROUT,
    MSPV_FWWIFI,
    MSPV_INJECTION_JOUR,
    MSPV_MANUBAL,
    MSPV_MANURAD,
    MSPV_MODELE,
    MSPV_OUTBAL,
    MSPV_OUTRAD,
    MSPV_OUTSTATS,
    MSPV_POWPV,
    MSPV_POWPV_CONS,
    MSPV_POWPV_INJ,
    MSPV_POWRESO,
    MSPV_PRODUCTION_CUMUL,
    MSPV_PRODUCTION_JOUR,
    MSPV_PRODUCTION_JOUR_CONS,
    MSPV_RSSI,
    MSPV_SERNUM,
    MSPV_SONDE_9,
    MSPV_SONDE_10,
    MSPV_SONDE_11,
    MSPV_SONDE_12,
    MSPV_SONDE_13,
    MSPV_SONDE_14,
    MSPV_SONDE_15,
    MSPV_SONDE_16,
    MSPV_SURVMM,
    MSPV_TAMB,
    MSPV_TBAL,
    MSPV_TEST_ROUTEUR,
    MSPV_TEST_ROUTEUR_OPTIONS,
    MSPV_TIME,
    MSPV_TSDB,
    MSPV_VERSION,
)

_LOGGER = logging.getLogger(__name__)


INANS_NBVAL = 16
PARAMSYS_NBVAL = 10
CPTVALS_NBVAL = 4
CPTVALS_NBVAL_4_4D = 6
CMDPOS_NBVAL = 8


class MsunPVApiClientError(Exception):
    """Exception to indicate a general API error."""


class MsunPVApiClientCommunicationError(
    MsunPVApiClientError,
):
    """Exception to indicate a communication error."""


class MsunPVApiClientAuthenticationError(
    MsunPVApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise MsunPVApiClientAuthenticationError(msg)
    response.raise_for_status()


def _hextoint(val: str) -> int:
    """Hex string to signed integer."""
    uintval = int(val, 16)
    bits = 4 * (len(val))
    if uintval >= 2 ** (bits - 1):
        uintval = int(0 - ((2**bits) - uintval))
    return uintval


class MsunPVApiClient:
    """Sample API Client."""

    _base_url: str
    _router_type: str
    _sondes_comp: bool
    _session: aiohttp.ClientSession
    _attributes: dict[str, Any]

    def __init__(
        self,
        url: str,
        router_type: str,
        sondes_comp: bool,  # noqa: FBT001
        session: aiohttp.ClientSession,
    ) -> None:
        """Init MSunPV API Client."""
        self._base_url: str = url
        self._router_type: str = router_type
        self._sondes_comp: bool = sondes_comp
        self._session: aiohttp.ClientSession = session
        self._attributes = {}

    def _decode_inans(self, doc: dict[str, Any]) -> None:
        # InAns - Valeurs des 16 sondes
        # <inAns>1157,6;1,0; 0; 0;215,0;61,8;0,0;0,0; 0; 0; 0; 0; 0; 0; 0; 0;</inAns>
        inans: str = doc["xml"]["inAns"]
        vals = inans.replace(",", ".").split(";")
        if len(vals) < INANS_NBVAL:
            msg = f"InAns - Nombre de sondes incorrect: {len(vals)}, vals= {vals}"
            raise ValueError(msg)

        self._attributes[MSPV_POWRESO] = float(vals[0])
        self._attributes[MSPV_POWPV] = -float(
            vals[1]
        )  # inverse pour l'avoir en positif

        # Valeurs fonction du type du routeur
        if self._router_type == MSPV_4_4D:
            self._attributes[MSPV_OUTBAL] = float(vals[2])  # Puissance en W
            self._attributes[MSPV_OUTRAD] = float(vals[3])  # Puissance en W
        elif self._router_type == MSPV_2_2D:
            self._attributes[MSPV_OUTBAL] = round(
                float(vals[2]) / 4
            )  # (0-400) -> (0-100%)
            self._attributes[MSPV_OUTRAD] = round(
                float(vals[3]) / 4
            )  # (0-400) -> (0-100%)

        self._attributes[MSPV_TBAL] = float(vals[5])
        self._attributes[MSPV_TSDB] = float(vals[6])
        self._attributes[MSPV_TAMB] = float(vals[7])

        # Sondes complémentaires génériques
        if self._sondes_comp:
            self._attributes[MSPV_SONDE_9] = float(vals[8])
            self._attributes[MSPV_SONDE_10] = float(vals[9])
            self._attributes[MSPV_SONDE_11] = float(vals[10])
            self._attributes[MSPV_SONDE_12] = float(vals[11])
            self._attributes[MSPV_SONDE_13] = float(vals[12])
            self._attributes[MSPV_SONDE_14] = float(vals[13])
            self._attributes[MSPV_SONDE_15] = float(vals[14])
            self._attributes[MSPV_SONDE_16] = float(vals[15])

    def _decode_paramsys(self, doc: dict[str, Any]) -> None:
        # paramSys -
        #   Heure; Date; enregistrement SD; intervalle enregistrement;
        #   nom projet; version; n° série; firmware wifi et routeur
        #   <paramSys>20:59:45;17/03/2025;On;01:00;0,0;
        #       MS_PV2_2d;5.0.1;0000200;104b;104b;00:00;00:00</paramSys>
        paramsys = doc["xml"]["paramSys"]
        vals = paramsys.replace(",", ".").split(";")
        if len(vals) < PARAMSYS_NBVAL:
            msg = f"paramSys - Nombre de paramètres système incorrect: {len(vals)}"
            raise ValueError(msg)
        self._attributes[MSPV_TIME] = vals[0]
        self._attributes[MSPV_DATE] = vals[1]
        self._attributes[MSPV_MODELE] = vals[5]  # modele du routeur
        self._attributes[MSPV_VERSION] = vals[6]  # version projet
        self._attributes[MSPV_SERNUM] = vals[7]  # Numero de serie
        self._attributes[MSPV_FWWIFI] = vals[8]  # Firmware wifi
        self._attributes[MSPV_FWROUT] = vals[9]  # Firmware routeur

    def _decode_cmdpos(self, doc: dict[str, Any]) -> None:
        # L'état des 8 commandes, en binaire sur 4 bits
        # <cmdPos>a;0;0;0;0;0;0;2;</cmdPos>
        cmdpos = doc["xml"]["cmdPos"]
        vals = cmdpos.split(";")
        if len(vals) < CMDPOS_NBVAL:
            msg = f"cmdPos - Nombre de commandes incorrect: {len(vals)}"
            raise ValueError(msg)

        val = int(vals[0], 16)
        self._attributes[MSPV_MANUBAL] = bool((val & 0x01) != 0)
        self._attributes[MSPV_AUTOBAL] = bool((val & 0x02) != 0)
        self._attributes[MSPV_MANURAD] = bool((val & 0x04) != 0)
        self._attributes[MSPV_AUTORAD] = bool((val & 0x08) != 0)

        val = int(vals[7], 16)
        if val in MSPV_TEST_ROUTEUR_OPTIONS:
            self._attributes[MSPV_TEST_ROUTEUR] = MSPV_TEST_ROUTEUR_OPTIONS[val]
        else:
            self._attributes[MSPV_TEST_ROUTEUR] = "undef"

    def _decode_cptvals(self, doc: dict[str, Any]) -> None:
        # Valeurs des 8 compteurs en hexadécimal
        # <cptVals>9702;ffffc0d9;fffe0040;fffff37c;0;0;0;0;</cptVals>
        cptvals = doc["xml"]["cptVals"]
        vals = cptvals.replace(",", ".").split(";")
        if len(vals) < CPTVALS_NBVAL:
            msg = f"cptVals - Nombre de compteurs incorrect: {len(vals)}"
            raise ValueError(msg)

        self._attributes[MSPV_CONSOMMATION_JOUR] = (
            float(
                _hextoint("00" + vals[0])
            )  # pad 0 à gauche,.update({ car toujourS positif
            / 10000.0  # de dixième de Wh, en kWh
        )
        self._attributes[MSPV_INJECTION_JOUR] = (
            float(_hextoint(vals[1])) / -10000.0  # de dixième de Wh, en kWh positif
        )
        self._attributes[MSPV_PRODUCTION_JOUR] = (
            float(_hextoint(vals[2])) / -10000.0  # de dixième de Wh, en kWh positif
        )
        self._attributes[MSPV_PRODUCTION_CUMUL] = (
            float(_hextoint(vals[3])) / -10.0  # de dixième de kWh, en kWh positif
        )

        # Compteurs spécifiques msunpv 4x4
        if self._router_type == MSPV_4_4D:
            if len(vals) < CPTVALS_NBVAL_4_4D:
                msg = f"cptVals - Nombre de compteurs incorrect: {len(vals)}"
                raise ValueError(msg)

            # Consommation cumulus journalière
            self._attributes[MSPV_CONSOMMATION_BALLON_JOUR] = (
                float(_hextoint(vals[4])) / 10000.0  # de dixième de Wh, en kWh positif
            )
            # Consommation radiateur journalière
            self._attributes[MSPV_CONSOMMATION_RADIATEUR_JOUR] = (
                float(_hextoint(vals[5])) / 10000.0  # de dixième de Wh, en kWh positif
            )

    def decode_status(
        self,
        payload: str,
        decod_option: int,
    ) -> None:
        """Decode data of status.xml."""
        _LOGGER.debug("decode_status - payload= %s", payload)
        doc = xmltodict.parse(payload)

        ## ----
        if decod_option & DECOD_OPTION_INANS:
            self._decode_inans(doc)
        if decod_option & DECOD_OPTION_PARAMSYS:
            self._decode_paramsys(doc)
        if decod_option & DECOD_OPTION_CMDPOS:
            self._decode_cmdpos(doc)
        if decod_option & DECOD_OPTION_CPTVALS:
            self._decode_cptvals(doc)

        # pas transmis sur les anciens routeurs (v<104)
        rssi = doc["xml"]["rssi"].split(";")[1] if "rssi" in doc["xml"] else 0
        self._attributes[MSPV_RSSI] = rssi

        # Surveillance des sondes:
        # <survMm>0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;</survMm>
        #   0 pas de dépassement,
        #   1 dépassement maxi,
        #   2 dépassement mini ou sonde déconnectée
        survmm = doc["xml"]["survMm"]
        self._attributes[MSPV_SURVMM] = survmm

        # Valeurs des 16 sorties de 0 à 100%
        # <outStat>0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;</outStat>
        outstat = doc["xml"]["outStat"]
        self._attributes[MSPV_OUTSTATS] = outstat

        # Valeurs calculées-e
        prod_j: float = self._attributes[MSPV_PRODUCTION_JOUR]
        inj_j: float = float(self._attributes[MSPV_INJECTION_JOUR])
        self._attributes[MSPV_PRODUCTION_JOUR_CONS] = prod_j - inj_j
        conso_j: float = self._attributes[MSPV_CONSOMMATION_JOUR]
        self._attributes[MSPV_CONSOMMATION_GLOBALE] = conso_j + prod_j - inj_j

        powreso = self._attributes[MSPV_POWRESO]
        powpv = self._attributes[MSPV_POWPV]
        powpv_inj = -powreso if (powpv >= 0.0 and powreso <= 0.0) else 0
        self._attributes[MSPV_POWPV_INJ] = powpv_inj
        self._attributes[MSPV_POWPV_CONS] = powpv - powpv_inj

        choutval = doc["xml"]["chOutVal"]
        self._attributes[MSPV_CHOUTVALS] = choutval

    async def async_get_status_xml_data(self) -> dict[str, Any]:
        """Get router data from status.xml."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method="get",
                    url=self._base_url + "/status.xml",
                )
                _verify_response_or_raise(response)

                payload: str = await response.text()
                self.decode_status(
                    payload=payload,
                    decod_option=DECOD_OPTION_ALL,
                )
                return self._attributes

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise MsunPVApiClientError(
                msg,
            ) from exception

    ##-----------------------------------------------

    async def async_set_command(self, cmd_num: int, mask1: int, mask2: int = 0) -> None:
        """Send command to router by the API."""
        _LOGGER.debug("async_set_command - %d, %d, %d", cmd_num, mask1, mask2)

        try:
            # Lecture de l'etat courant des commandes
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method="get",
                    url=self._base_url + "/status.xml",
                )
                _verify_response_or_raise(response)

                payload: str = await response.text()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise MsunPVApiClientError(
                msg,
            ) from exception

        doc = xmltodict.parse(payload)

        # L'état des 8 commandes, en binaire sur 4 bits
        # <cmdPos>a;0;0;0;0;0;0;2;</cmdPos>
        cmdpos: str = doc["xml"]["cmdPos"]
        _LOGGER.debug("async_set_command - cmdPos= [%s]", cmdpos)
        cmdpos = cmdpos.strip()
        vals: list[str] = cmdpos.split(";")
        if len(vals) < CMDPOS_NBVAL:
            msg = f"cmdPos - Nombre de valeurs incorrect: {len(vals)}"
            raise ValueError(msg)

        # Construction de la commande
        buff: str = ""
        for ii, val in enumerate(vals):
            if ii < CMDPOS_NBVAL:
                newval: str = (
                    str((int(val, 16) & mask1) | mask2)
                    if ii == cmd_num
                    else str(int(val, 16))
                )
                buff += f"{newval};"

        # Envoi de la commande
        try:
            _LOGGER.debug("async_set_command - parS=%s", buff)

            # Urlencoded data
            form_data = aiohttp.FormData()
            form_data.add_field("parS", buff)
            _LOGGER.debug("async_set_command - urlencoded : [%s]", form_data)

            response: aiohttp.ClientResponse = await self._session.request(
                method="post",
                url=self._base_url + "/index.xml",
                data=form_data,
            )
            _verify_response_or_raise(response)
            payload: str = await response.text("ISO-8859-1")
            _LOGGER.debug("post - status= %d, response= %s", response.status, payload)

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise MsunPVApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise MsunPVApiClientError(
                msg,
            ) from exception

    async def async_set_manu_bal_on(self) -> None:
        """Set manu Bal on."""
        await self.async_set_command(
            cmd_num=CMD_MANU_BAL[0], mask1=CMD_MANU_BAL[1], mask2=CMD_MANU_BAL[2]
        )

    async def async_set_manu_bal_off(self) -> None:
        """Set manu bal off."""
        await self.async_set_command(cmd_num=CMD_MANU_BAL[0], mask1=CMD_MANU_BAL[1])

    async def async_set_auto_bal_on(self) -> None:
        """Set auto bal on."""
        await self.async_set_command(
            cmd_num=CMD_AUTO_BAL[0], mask1=CMD_AUTO_BAL[1], mask2=CMD_AUTO_BAL[2]
        )

    async def async_set_auto_bal_off(self) -> None:
        """Set auto bal off."""
        await self.async_set_command(cmd_num=CMD_AUTO_BAL[0], mask1=CMD_AUTO_BAL[1])

    async def async_set_manu_rad_on(self) -> None:
        """Set manu rad on."""
        await self.async_set_command(
            cmd_num=CMD_MANU_RAD[0], mask1=CMD_MANU_RAD[1], mask2=CMD_MANU_RAD[2]
        )

    async def async_set_manu_rad_off(self) -> None:
        """Set manu rad off."""
        await self.async_set_command(cmd_num=CMD_MANU_RAD[0], mask1=CMD_MANU_RAD[1])

    async def async_set_auto_rad_on(self) -> None:
        """Set auto rad on."""
        await self.async_set_command(
            cmd_num=CMD_AUTO_RAD[0], mask1=CMD_AUTO_RAD[1], mask2=CMD_AUTO_RAD[2]
        )

    async def async_set_auto_rad_off(self) -> None:
        """Set auto rad off."""
        await self.async_set_command(cmd_num=CMD_AUTO_RAD[0], mask1=CMD_AUTO_RAD[1])

    async def async_set_test_routeur_inject(self) -> None:
        """Set test routeur to inject."""
        _LOGGER.debug("set_test_routeur_inject")
        await self.async_set_command(
            cmd_num=CMD_TEST_ROUTEUR_INJECTION[0],
            mask1=CMD_TEST_ROUTEUR_INJECTION[1],
            mask2=CMD_TEST_ROUTEUR_INJECTION[2],
        )

    async def async_set_test_routeur_zero(self) -> None:
        """Set test routeur inject to zero."""
        _LOGGER.debug("set_test_routeur_zero")
        await self.async_set_command(
            cmd_num=CMD_TEST_ROUTEUR_ZERO[0],
            mask1=CMD_TEST_ROUTEUR_ZERO[1],
            mask2=CMD_TEST_ROUTEUR_ZERO[2],
        )

    async def async_set_test_routeur_moyen(self) -> None:
        """Set test routeur inject to moyen."""
        _LOGGER.debug("set_test_routeur_moyen")
        await self.async_set_command(
            cmd_num=CMD_TEST_ROUTEUR_MOYEN[0],
            mask1=CMD_TEST_ROUTEUR_MOYEN[1],
            mask2=CMD_TEST_ROUTEUR_MOYEN[2],
        )

    async def async_set_test_routeur_fort(self) -> None:
        """Set test routeur inject to fort."""
        _LOGGER.debug("set_test_routeur_fort")
        await self.async_set_command(
            cmd_num=CMD_TEST_ROUTEUR_FORT[0],
            mask1=CMD_TEST_ROUTEUR_FORT[1],
            mask2=CMD_TEST_ROUTEUR_FORT[2],
        )
