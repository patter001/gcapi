from enum import IntEnum


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
