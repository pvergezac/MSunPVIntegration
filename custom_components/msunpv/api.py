"""Sample API Client."""

from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Any

import aiohttp
import async_timeout
import xmltodict

from .const import LOGGER, MSPV_2_2d, MSPV_4_4d


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
        raise MsunPVApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


def _hextoint(val: str) -> int:
    """Hex string to signed integer."""
    uintval = int(val, 16)
    bits = 4 * (len(val))
    if uintval >= 2 ** (bits - 1):
        uintval = int(0 - ((2**bits) - uintval))
    return uintval


@dataclass
class MSunPVApiData:
    """Class pour mémorisé les données du MSunPV."""

    # Le type du routeur 2x2, 4x4, saisi à la config
    _router_type: str
    _sondes_comp: bool

    """Les mesures et sondes."""
    powreso: float
    powpv: float
    outbal: float
    outrad: float
    tbal: float
    tsdb: float
    tamb: float

    powpv_inj: float
    powpv_cons: float

    """Les cumuls journaliers et globaux"""
    consommation_jour: float
    injection_jour: float
    production_jour: float
    production_cumul: float
    production_jour_cons: float  # Production solaire consommée (PV - injection)
    consommation_globale: float  # Consomation globale (reseau + PV - injection)

    conso_ballon_jour: float  # Consommation cumulus journalière (Msunpv 4x4)
    conso_radiateur_jour: float  # Consommation radiateur journalière (Msunpv 4x4)

    """Les param sys"""
    date: str
    time: str
    modele: str
    version: str
    sernum: str
    fwrout: str
    fwwifi: str

    """Les surveillance"""
    survmm: str

    """Les commandes"""
    cmdpos: str

    manubal: bool
    autobal: bool
    manurad: bool
    autorad: bool

    etat_test_routeur_inject: bool
    etat_test_routeur_zero: bool
    etat_test_routeur_moyen: bool
    etat_test_routeur_fort: bool

    """Les etats des sorties"""
    outstats: str

    """Les valeurs calculées en sortie des modules chauffage """
    choutvals: str

    sonde_8: float = 0
    sonde_9: float = 0
    sonde_10: float = 0
    sonde_11: float = 0
    sonde_12: float = 0
    sonde_13: float = 0
    sonde_14: float = 0
    sonde_15: float = 0
    rssi: int = 0

    def __xxxstr__(self) -> str:
        """Printable str of object."""
        vars(self)
        _aaa: str = ""
        for attr in dir(vars):
            _aaa += attr + ": " + getattr(self, attr)

        return _aaa

    def get(self, attribute: str) -> Any:
        """Getter of attributes."""
        return self.__getattribute__(attribute)

    def __init__(self, router_type: str, sondes_comp: bool, payload: str) -> None:  # noqa: FBT001, PLR0915
        """Init a partir des donnée XML reçues."""
        self._router_type = router_type
        self._sondes_comp = sondes_comp
        LOGGER.debug(
            "INIT MSunPVApiData - router_type= '%s', sondes_comp= '%r'",
            router_type,
            sondes_comp,
        )

        doc = xmltodict.parse(payload)
        LOGGER.debug("doc keys= " + str(doc["xml"].keys()))

        # InAns - Valeurs des 16 sondes
        # <inAns>1157,6;1,0; 0; 0;215,0;61,8;0,0;0,0; 0; 0; 0; 0; 0; 0; 0; 0;</inAns>
        inans: str = doc["xml"]["inAns"]
        vals = inans.replace(",", ".").split(";")
        self.powreso = float(vals[0])
        self.powpv = 0.0 - float(vals[1])  # inverse pour l'avoir en positif

        # Valeurs fonction du type du routeur
        if self._router_type == MSPV_4_4d:
            LOGGER.debug("Décode sondes pour MSPV 4x4")
            self.outbal = float(vals[2])  # Puissance en W
            self.outrad = float(vals[3])  # Puissance en W
        elif self._router_type == MSPV_2_2d:
            LOGGER.debug("Décode sondes pour MSPV 2x2")
            self.outbal = round(float(vals[2]) / 4)  # (0-400) -> (0-100%)
            self.outrad = round(float(vals[3]) / 4)  # (0-400) -> (0-100%)

        self.tbal = float(vals[5])
        self.tsdb = float(vals[6])
        self.tamb = float(vals[7])

        # Sondes complémentaires génériques
        if self._sondes_comp:
            LOGGER.debug("Décode sondes complementaires")
            self.sonde_8 = float(vals[8])
            self.sonde_9 = float(vals[9])
            self.sonde_10 = float(vals[10])
            self.sonde_11 = float(vals[11])
            self.sonde_12 = float(vals[12])
            self.sonde_13 = float(vals[13])
            self.sonde_14 = float(vals[14])
            self.sonde_15 = float(vals[15])

        # paramSys -
        #   Heure; Date; enregistrement SD; intervalle enregistrement;
        #   nom projet; version; n° série; firmware wifi et routeur
        #   <paramSys>20:59:45;17/03/2025;On;01:00;0,0;
        #       MS_PV2_2d;5.0.1;0000200;104b;104b;00:00;00:00</paramSys>
        paramsys = doc["xml"]["paramSys"]
        vals = paramsys.replace(",", ".").split(";")
        self.time = vals[0]
        self.date = vals[1]
        self.modele = vals[5]  # modele du routeur ("MS_PV2_2d", "MS_PV4_4d")
        self.version = vals[6]  # version projet
        self.sernum = vals[7]  # Numero de serie
        self.fwwifi = vals[8]  # Firmware wifi
        self.fwrout = vals[9]  # Firmware routeur

        if "rssi" in doc["xml"]:  # pas transmis sur les anciens routeurs (v<104)
            self.rssi = doc["xml"]["rssi"].split(";")[1]
        else:
            self.rssi = 0

        # Surveillance des sondes:
        #   0 pas de dépassement,
        #   1 dépassement maxi,
        #   2 dépassement mini ou sonde déconnectée
        # <survMm>0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;</survMm>
        survmm = doc["xml"]["survMm"]
        self.survmm = survmm

        # L'état des 8 commandes, en binaire sur 4 bits
        # <cmdPos>a;0;0;0;0;0;0;2;</cmdPos>
        cmdpos = doc["xml"]["cmdPos"]
        self.cmdpos = cmdpos

        val = int(cmdpos.split(";")[0], 16)
        self.manubal = (val & 0x01) != 0
        self.autobal = (val & 0x02) != 0
        self.manurad = (val & 0x04) != 0
        self.autorad = (val & 0x08) != 0

        val = int(cmdpos.split(";")[7], 16)
        self.etat_test_routeur_inject = (val & 0x01) != 0
        self.etat_test_routeur_zero = (val & 0x02) != 0
        self.etat_test_routeur_moyen = (val & 0x04) != 0
        self.etat_test_routeur_fort = (val & 0x08) != 0

        # Valeurs des 16 sorties de 0 à 100%
        # <outStat>0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;</outStat>
        outstat = doc["xml"]["outStat"]
        self.outstats = outstat

        # Valeurs des 8 compteurs en hexadécimal
        # <cptVals>9702;ffffc0d9;fffe0040;fffff37c;0;0;0;0;</cptVals>
        cptvals = doc["xml"]["cptVals"]
        vals = cptvals.replace(",", ".").split(";")
        self.consommation_jour = (
            float(_hextoint("00" + vals[0]))  # pad 0 à gauche, car toujourS positif
            / 10000.0  # de dixième de Wh, en kWh
        )
        self.injection_jour = (
            float(_hextoint(vals[1])) / -10000.0  # de dixième de Wh, en kWh positif
        )
        self.production_jour = (
            float(_hextoint(vals[2])) / -10000.0  # de dixième de Wh, en kWh positif
        )
        self.production_cumul = (
            float(_hextoint(vals[3])) / -10.0  # de dixième de kWh, en kWh positif
        )

        # Compteurs spécifiques msunpv 4x4
        if self._router_type == MSPV_4_4d:
            # Consommation cumulus journalière
            self.conso_ballon_jour = (
                float(_hextoint(vals[4])) / 10000.0  # de dixième de Wh, en kWh positif
            )
            # Consommation radiateur journalière
            self.conso_radiateur_jour = (
                float(_hextoint(vals[5])) / 10000.0  # de dixième de Wh, en kWh positif
            )

        # Valeurs calculées
        self.production_jour_cons = self.production_jour - self.injection_jour
        self.consommation_globale = self.consommation_jour + self.production_jour_cons
        self.powpv_inj = (
            -self.powreso if (self.powpv >= 0.0 and self.powreso <= 0.0) else 0
        )
        self.powpv_cons = self.powpv - self.powpv_inj

        choutval = doc["xml"]["chOutVal"]
        self.choutvals = choutval


class MsunPVApiClient:
    """Sample API Client."""

    _base_url: str
    _router_type: str
    _sondes_comp: bool
    _session: aiohttp.ClientSession

    def __init__(
        self,
        url: str,
        router_type: str,
        sondes_comp: bool,  # noqa: FBT001
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._base_url = url
        self._router_type = router_type
        self._sondes_comp = sondes_comp
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + "/status.xml",
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)

                payload: str = await response.text()
                return MSunPVApiData(
                    router_type=self._router_type,
                    sondes_comp=self._sondes_comp,
                    payload=payload,
                )

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
