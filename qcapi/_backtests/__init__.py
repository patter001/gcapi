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
    
    def create(self, project_id: str, compile_id: str, backtest_name, parameters: dict|None):
        ...
        # parameters syntax in to json is a bit odd:
        #  "parameters[name]": "parameters[ema_fast] = 10, parameters[ema_slow] = 100"
        endpoint_params = dict(projectId=project_id, compileId=compile_id, backtestName=backtest_name)
        if parameters is not None:
            params_string = []
            for k, v in parameters.items():
                params_string.append(f"parameters[{k}] = {v}")
            endpoint_params["parameters[name]"] = ", ".join(params_string)
        return self._client.request(
            "POST",
            f"{self._url}/create",
            json=endpoint_params,
            # response_type=BacktestSummaryResponse,
        )
 