"""Sample API Client."""

from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Any

import aiohttp
import async_timeout
import xmltodict

from .const import LOGGER


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

    """Les mesures et sondes."""
    powreso: float
    powpv: float
    outbal: int
    outrad: int
    tbal: float
    tsdb: float
    tamb: float

    """Les cumuls journaliers et globaux"""
    consommation_jour: float
    injection_jour: float
    production_jour: float
    production_cumul: float

    """Les param sys"""
    date: str
    time: str
    modele: str
    version: str
    sernum: str
    rssi: int

    """Les surveillance"""
    survmm: str

    """Les commandes"""
    cmdpos: str

    """Les etats des sorties"""
    outstats: str

    """Les valeurs calculées en sortie des modules chauffage """
    choutvals: str

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

    def __init__(self, payload: str) -> None:
        """Init a partir des donnée XML reçues."""
        LOGGER.debug("payload= " + payload)
        doc = xmltodict.parse(payload)
        LOGGER.debug("doc keys= " + str(doc["xml"].keys()))
        LOGGER.debug("doc items= " + str(doc["xml"].items()))

        inans: str = doc["xml"]["inAns"]
        LOGGER.debug("inans= " + inans)

        vals = inans.replace(",", ".").split(";")
        self.powreso = float(vals[0])
        self.powpv = 0.0 - float(vals[1])  # inverse pour l'avoir en positif
        self.outbal = int(float(vals[2]) / 4)  # (0-400) -> (0-100%)
        self.outrad = int(float(vals[3]) / 4)  # (0-400) -> (0-100%)
        self.tbal = float(vals[5])
        self.tsdb = float(vals[6])
        self.tamb = float(vals[7])

        paramsys = doc["xml"]["paramSys"]
        vals = paramsys.replace(",", ".").split(";")
        self.time = vals[0]
        self.date = vals[1]
        self.modele = vals[5]  # modele du routeur ("MS_PV2_2d", "MS_PV4_4d")
        self.version = vals[6]  # version
        self.sernum = vals[7]  # Numero de serie

        self.rssi = doc["xml"]["rssi"].split(";")[1]

        survmm = doc["xml"]["survMm"]
        self.survmm = survmm

        cmdpos = doc["xml"]["cmdPos"]
        self.cmdpos = cmdpos

        outstat = doc["xml"]["outStat"]
        self.outstats = outstat

        cptvals = doc["xml"]["cptVals"]
        vals = cptvals.replace(",", ".").split(";")
        self.consommation_jour = (
            float(_hextoint("00" + vals[0]))  # pad 0 à gauche, car toujour positif
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

        choutval = doc["xml"]["chOutVal"]
        self.choutvals = choutval


class MsunPVApiClient:
    """Sample API Client."""

    def __init__(
        self,
        url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._base_url = url
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + "/status.xml",
        )

    #    async def async_set_title(self, value: str) -> Any:
    #        """Get data from the API."""
    #        return await self._api_wrapper(
    #            method="patch",
    #            url=self._base_url,
    #            data={"title": value},
    #            headers={"Content-type": "application/json; charset=UTF-8"},
    #        )

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
                LOGGER.debug("reponse payload: " + payload)

                ms = MSunPVApiData(payload=payload)
                LOGGER.debug("ms : " + str(ms))
                return ms

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
