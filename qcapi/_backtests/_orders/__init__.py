from __future__ import annotations

from typing import TYPE_CHECKING, List
from pydantic import BaseModel
from ...models import Order

if TYPE_CHECKING:
    from ..._client import QCClient


class OrdersEndpoint:
    def __init__(self, client: "QCClient", url: str):
        self._client = client
        self._url = url

    def read(self, project_id, backtest_id, start=0, end=100) -> BacktestOrdersResponse:
        if (end - start) > 100:
            raise ValueError("You can only request 100 at a time")
        # typing not familiar with  response type
        return self._client.request(
            "GET",
            f"{self._url}/read",
            json=dict(projectId=project_id, backtestId=backtest_id, start=start, end=end),
            response_type=BacktestOrdersResponse,
        )

    def read_all(self, project_id, backtest_id) -> List["Order"]:
        batch_size = 100
        start = 0
        end = start + batch_size
        orders = order_batch = self.read(project_id, backtest_id, start, end).orders
        breakpoint()
        while len(order_batch) >= batch_size:
            start += batch_size
            end += batch_size
            order_batch = self.read(project_id, backtest_id, start, end).orders
            orders.extend(order_batch)
        return orders


class BacktestOrdersResponse(BaseModel):
    orders: list[Order]
    length: int


"""
class OrderStatusEnum(Enum):
    NEW = 0
    SUBMITTED = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 5
    # Add other options...

class SecurityTypeEnum(Enum):
    BASE = 0
    EQUITY = 1
    OPTION = 2
    COMMODITY = 3
    # Add other options...

class DirectionEnum(Enum):
    BUY = 0
    SELL = 1
    HOLD = 2
    # Add other options...

"""
