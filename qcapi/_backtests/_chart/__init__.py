from __future__ import annotations

from typing import TYPE_CHECKING 
from pydantic import BaseModel

from ...models import Chart 

if TYPE_CHECKING:
    from ..._client import QCClient


class ChartEndpoint:
    def __init__(self, client: "QCClient", url: str):
        self._client = client
        self._url = url

    def read(
        self, project_id, backtest_id, name: str, count: int, start: int | None = None, end: int | None = None
    ) -> ReadChartResponse:
        """
        name: Chart to request
        count: the number of data points to request
        start: the UTC timestamp start seconds of the request
        end: the UTC timestamp end seconds of the request
        """
        params = dict(projectId=project_id, backtestId=backtest_id, name=name, count=count)
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._client.request("GET", f"{self._url}/read", json=params, response_type=ReadChartResponse)


class ReadChartResponse(BaseModel):
    chart: "Chart | None" = None
    progress: int | None = None
    success: bool
    errors: list[str] | None = None


