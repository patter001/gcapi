from typing import TYPE_CHECKING, Any
from ..models import BacktestSummaryResponse , BacktestResponse
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
            response_type=BacktestSummaryResponse ,
        )
    
    def create(self, project_id: str | int, compile_id: str, backtest_name, parameters: dict|None):
        ...
        # parameters syntax in to json is a bit odd:
        #  "parameters[name]": "parameters[ema_fast] = 10, parameters[ema_slow] = 100"
        endpoint_params: dict[str, Any] = dict(projectId=project_id, compileId=compile_id, backtestName=backtest_name)
        if parameters is not None:
            endpoint_params['parameters'] = parameters
        return self._client.request(
            "POST",
            f"{self._url}/create",
            json=endpoint_params,
            response_type=BacktestResponse,
        )

    def read(self, project_id: str | int, backtest_id: str, chart: str | None = None):
        if chart is not None:
            params = dict(projectId=project_id, backtestId=backtest_id, chart=chart)
        else:
            params = dict(projectId=project_id, backtestId=backtest_id)
        return self._client.request(
            "GET",
            f"{self._url}/read",
            json=params,
            response_type=BacktestResponse,
        )

    def delete(self, project_id: str | int, backtest_id: str):
        return self._client.request(
            "DELETE",
            f"{self._url}/delete",
            json=dict(projectId=project_id, backtestId=backtest_id),
            response_type=None,
        )