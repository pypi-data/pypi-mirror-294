from __future__ import annotations

from typing import Any, Optional, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ogmios.client import Client

from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.logger import logger
from ogmios.datatypes import Origin, Point
import ogmios.response_handler as rh
import ogmios.model.ogmios_model as om
import ogmios.model.model_map as mm

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


class QueryLedgerTip:
    """Ogmios method to query the point of the ledger's latest block.

    NOTE: This class is not intended to be used directly. Instead, use the Client.query_ledger_tip
    method.

    :param client: The client to use for the request.
    :type client: Client
    """

    def __init__(self, client: Client):
        self.client = client
        self.method = mm.Method.queryLedgerState_tip.value

    def execute(self, id: Optional[Any] = None) -> Tuple[Union[Point, Origin], Optional[Any]]:
        """Send and receive the request.

        :param id: The ID of the request.
        :type id: Any
        :return: The tip or origin and ID of the response.
        :rtype: (Tip | Origin, Optional[Any])
        """
        self.send(id)
        return self.receive()

    def send(self, id: Optional[Any] = None) -> None:
        """Send the request.

        :param id: The ID of the request.
        :type id: Any
        """
        pld = om.QueryLedgerStateTip(
            jsonrpc=self.client.rpc_version,
            method=self.method,
            id=id,
        )
        self.client.send(pld.json())

    def receive(self) -> Tuple[Union[Point, Origin], Optional[Any]]:
        """Receive a previously requested response.

        :return: The tip or origin and ID of the response.
        :rtype: (Tip | Origin, Optional[Any])
        """
        response = self.client.receive()
        return self._parse_QueryLedgerTip_response(response)

    @staticmethod
    def _parse_QueryLedgerTip_response(
        response: dict,
    ) -> Tuple[Union[Point, Origin], Optional[Any]]:
        if response.get("method") != mm.Method.queryLedgerState_tip.value:
            raise InvalidMethodError(f"Incorrect method for query_ledger_tip response: {response}")

        if response.get("error"):
            raise ResponseError(f"Ogmios responded with error: {response}")

        if result := response.get("result"):
            point: Union[Point, Origin] = rh.parse_PointOrOrigin(result)
            id: Optional[Any] = response.get("id")
            logger.info(
                f"""Parsed query_ledger_tip response:
        Point = {point}
        ID = {id}"""
            )
            return point, id
        raise InvalidResponseError(f"Failed to parse query_ledger_tip response: {response}")
