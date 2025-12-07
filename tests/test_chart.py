import pytest
from qcapi import QCClient
from conftest import project_id, qc_client, chart_backtest_id


def test_chart_read(qc_client: QCClient, project_id: str, chart_backtest_id: str):
    qc_client.backtests.chart.read(project_id, chart_backtest_id, "Strategy Equity", 1000)
