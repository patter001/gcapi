from typing import TYPE_CHECKING
from ..models import BacktestSummaryResponse
from ._orders import OrdersEndpoint

if TYPE_CHECKING:
    from .._client import QCClient


class Backtests:
    def __init__(self, client: "QCClient", url):
        self._client = client
        self._url = url
        self.orders = OrdersEndpoint(client, url + "/orders")

    def list(self, project_id=0, include_statistics=True):
        return self._client.request(
            "GET",
            f"{self._url}/list",
            json=dict(projectId=project_id, includeStatistics=include_statistics),
            response_type=BacktestSummaryResponse,
        )
