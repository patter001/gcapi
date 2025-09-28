# https://www.quantconnect.com/docs/v2/cloud-platform/api-reference/backtest-management/list-backtests

from __future__ import annotations
from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

# parameter set is just a dict
ParameterSet = dict | list


class BacktestSummaryResult(BaseModel):
    backtestId: str
    status: str
    note: Optional[str]
    name: str
    created: str
    result: Optional[str]
    progress: int
    optimizationId: Optional[str]
    tradeableDates: Optional[int]  # was supposed to be a string
    parameterSet: Optional[ParameterSet]
    tags: list[str]
    sharpeRatio: float
    alpha: float
    beta: float
    compoundingAnnualReturn: float
    drawdown: float
    lossRate: float
    netProfit: float
    parameters: int
    psr: float
    securityTypes: Optional[int]  # was supposed to be a string, but found an int
    sortinoRatio: Optional[float]
    trades: int
    treynorRatio: float
    winRate: float


class BacktestSummaryResponse (BaseModel):
    backtests: list[BacktestSummaryResult]
    count: int
    success: bool
    errors: list[str] = []
