# gcapi

Project for 

# Getting started

## Instal

`pip install .`

To install to whatever python you environment you are using

You must set `USER_ID` and `TOKEN` for usage

# Example usage

I recommend install python-dotenv and putting your username and key in a .env file


```bash
echo USER_ID=user_id > .env
echo TOKEN=token >> .env
pip install python-dotenv
```

## Create client

```python
client = QCClient("https://www.quantconnect.com/api/v2", os.environ['USER_ID'], os.environ['TOKEN'])
```

From there the API should mostly match the end points in the web docs:

```python
client.backtests.list(project_id=project_id)
for bt in resp.backtests:
    print(f"{bt.backtestId} - {bt.name}")
```

## Start a backtest

- compile project to get a compileId
- read the compile until you result is complete
- kick off backtest

```python
project_id = "12345
response = client.compile.create(project_id)
backtest = client.backtests.create(project_id, response.compileId, "backtest name", {param1: "SPY"} )
```