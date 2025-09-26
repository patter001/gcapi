from __future__ import annotations
from typing import Optional, List
from enum import Enum, IntEnum
from datetime import datetime
from pydantic import BaseModel


class GroupOrderManager(BaseModel):
    id: int
    quantity: float
    count: int
    limitPrice: float
    orderIds: list[int]
    direction: int


class OrderSubmissionData(BaseModel):
    bidPrice: float
    askPrice: float
    lastPrice: float


class OrderEventStatus(Enum):
    NEW = "new"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partiallyFilled"
    FILLED = "filled"
    CANCELED = "canceled"
    INVALID = "invalid"
    CANCEL_PENDING = "cancelPending"
    UPDATE_SUBMITTED = "updateSubmitted"


class OrderStatus(IntEnum):
    NEW = 1
    SUBMITTED = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 5
    NONE = 6
    INVALID = 7
    CANCEL_PENDING = 8
    UPDATE_SUBMITTED = 9


# not enough info for this one
OrderProperties = dict


class OrderEvent(BaseModel):
    algorithmId: str
    symbol: str
    symbolValue: str
    symbolPermtick: str
    orderId: int
    orderEventId: int
    id: str
    status: OrderEventStatus
    orderFeeAmount: Optional[float] = None
    orderFeeCurrency: Optional[str] = None
    fillPrice: float
    fillPriceCurrency: str
    fillQuantity: float
    direction: str
    message: Optional[str]
    isAssignment: bool
    stopPrice: Optional[float] = None
    limitPrice: Optional[float] = None
    quantity: float
    time: float  # Unix timestamp
    isInTheMoney: Optional[bool] = None


class OrderTypeEnum(Enum):
    MARKET = 0
    LIMIT = 1
    STOP_MARKET = 2
    STOP_LIMIT = 3


class Symbol(BaseModel):
    value: str
    id: str
    permtick: str


class Order(BaseModel):
    id: int
    contingentId: Optional[int] = None
    brokerId: List[str]
    symbol: Symbol
    limitPrice: Optional[float] = None
    stopPrice: Optional[float] = None
    stopTriggered: Optional[bool] = None
    price: float
    priceCurrency: str
    time: datetime
    createdTime: datetime
    lastFillTime: Optional[datetime] = None
    lastUpdateTime: Optional[datetime] = None
    canceledTime: Optional[datetime] = None
    quantity: float
    type: int  # Enum can be used here for the order type
    status: OrderStatus  # Enum can be used here for the order status
    tag: Optional[str] = None
    securityType: int  # Enum can be used here for the security type
    direction: int  # Enum can be used here for the direction
    value: float
    orderSubmissionData: Optional["OrderSubmissionData"] = None
    isMarketable: bool
    properties: "OrderProperties"
    events: List[OrderEvent]
    trailingAmount: Optional[float] = None
    trailingPercentage: Optional[bool] = None
    groupOrderManager: Optional[GroupOrderManager] = None
    triggerPrice: Optional[float] = None
    triggerTouched: Optional[bool] = None
