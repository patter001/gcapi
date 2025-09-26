from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel
from ..models import Order

if TYPE_CHECKING:
    from .._client import QCClient


class LiveOrdersEndpoint:
    def __init__(self, client: "QCClient", url):
        self._client = client
        self._url = url

    def read(self, project_id, start=0, end=100) -> LiveOrdersResponse:
        return self._client.request(
            "GET",
            f"{self._url}/read",
            json=dict(start=start, end=end, projectId=project_id),
            response_type=LiveOrdersResponse,
        )

    def read_all(self, project_id) -> List["Order"]:
        batch_size = 100
        start = 0
        end = start + batch_size
        orders = order_batch = self.read(project_id, start, end).orders
        while len(order_batch) >= batch_size:
            start += batch_size
            end += batch_size
            order_batch = self.read(project_id, start, end).orders
            orders.extend(order_batch)
        return orders


class LiveOrdersResponse(BaseModel):
    orders: list[Order]
    length: int
    success: bool
    errors: Optional[list[str]] = None
