from dotenv import load_dotenv
from qcapi import QCClient
import os
import pytest

load_dotenv()


@pytest.fixture
def qc_client():
    return QCClient("https://www.quantconnect.com/api/v2", os.environ["USER_ID"], os.environ["TOKEN"])


@pytest.fixture
def project_id():
    return os.environ["TEST_PROJECT_ID"]


@pytest.fixture
def chart_backtest_id():
    return os.environ["TEST_CHART_BACKTEST_ID"]
