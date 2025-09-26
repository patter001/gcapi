from typing import TYPE_CHECKING
from ..models import BacktestSummaryResponse
from ._orders import LiveOrdersEndpoint

if TYPE_CHECKING:
    from .._client import QCClient


class LiveEndpoint:
    def __init__(self, client: "QCClient", url):
        self._client = client
        self._url = url
        self.orders = LiveOrdersEndpoint(client, self._url + "/orders")
