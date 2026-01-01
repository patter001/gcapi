from functools import cache
import time
from qcapi import QCClient
from qcapi.models import ChartSeriesTypeEnum
from pathlib import Path
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from datetime import datetime


load_dotenv()


@cache
def get_client():
    return QCClient("https://www.quantconnect.com/api/v2", os.environ["USER_ID"], os.environ["TOKEN"])


def run_backtest(project_id: str | int, output_dir: Path, test_name: str, parameters: dict, delete_after: bool = True):
    output_dir.mkdir(parents=True, exist_ok=True)
    client = get_client()
    response = client.compile.create(project_id)
    while response.state != "BuildError" and response.state != "BuildSuccess":
        print(f"Compile state: {response.state}")
        time.sleep(1)
        response = client.compile.read(project_id, response.compileId)

    # iterate params?
    response = client.backtests.create(project_id, response.compileId, test_name, parameters=parameters)
    completed = False
    print(f"Status: {response.backtest.status}")
    while not completed:
        status = client.backtests.read(project_id, response.backtest.backtest_id)
        completed = status.backtest.completed
        print(f"Status: {status.backtest.status}")
        time.sleep(5)

    with open(output_dir / f"{test_name}.json", "w") as f:
        f.write(status.model_dump_json(indent=3))

    if delete_after:
        client.backtests.delete(project_id, response.backtest.backtest_id)


def draw_chart(project_id, backtest_id, chart_name, series_name):
    client = get_client()
    # note: the count needs to be quite large due to equity having multiple per points per day
    resp = client.backtests.chart.read(project_id, backtest_id, chart_name, 50_000)
    if resp.chart is None:
        raise RuntimeError("Missing chart daa")
    traces = []
    for name, series in resp.chart.series.items():
        print(name)
        print(len(series.values))
        if series.seriesType == ChartSeriesTypeEnum.Line:
            trace = go.Scatter(
                x=[datetime.fromtimestamp(t[0]) for t in series.values],
                y=[t[1] for t in series.values],
                mode="lines",
                name=series.name,
            )
            traces.append(trace)
        elif series.seriesType == ChartSeriesTypeEnum.Candle:
            # Create candlestick trace
            trace = go.Candlestick(
                x=[datetime.fromtimestamp(t[0]) for t in series.values],
                open=[t[1] for t in series.values],
                high=[t[2] for t in series.values],
                low=[t[3] for t in series.values],
                close=[t[4] for t in series.values],
                name=series.name,
            )
            traces.append(trace)
        elif series.seriesType == ChartSeriesTypeEnum.Scatter:
            marker = "triangle-up" if series.scatterMarkerSymbol == "triangle" else series.scatterMarkerSymbol
            trace = go.Scatter(
                x=[datetime.fromtimestamp(t["x"]) for t in series.values],
                y=[t["y"] for t in series.values],
                mode="markers",
                name=series.name,
                marker=dict(symbol=marker, size=10),
            )
            traces.append(trace)
        elif series.seriesType == ChartSeriesTypeEnum.Bar:
            # not supported yet
            continue
        else:
            breakpoint()
    fig = go.Figure(traces)
    fig.show()
