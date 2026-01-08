from enum import IntEnum
from typing import Literal
from pydantic import BaseModel

class ChartTypeEnum(IntEnum):
    Overlay = 0
    Stacked = 1


class ChartSeriesTypeEnum(IntEnum):
    Line = 0
    Scatter = 1
    Candle = 2
    Bar = 3
    Flag = 4
    StackedArea = 5
    Pie = 6
    Treemap = 7

class Chart(BaseModel):
    name: str
    # this is what documentation states, but we seem to get an int instead
    chartType: ChartTypeEnum
    series: dict[str, "ChartSeries"]


class ChartSeries(BaseModel):
    name: str
    unit: str
    """Axis for the chart series."""
    values: list
    index: int
    """Index/position of the series on the chart."""
    seriesType: ChartSeriesTypeEnum
    color: str | None = None
    scatterMarkerSymbol: Literal["none", "circle", "square", "diamond", "triangle", "triangle-down"] | None = None
    """Confirmed this is a string"""
