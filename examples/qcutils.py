from functools import cache
import time
from qcapi import QCClient
from pathlib import Path
from dotenv import load_dotenv
import os

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
