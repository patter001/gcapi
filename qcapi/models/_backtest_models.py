from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


# ============== REQUEST MODELS ==============

class CreateBacktestRequest(BaseModel):
    """Request to create a new backtest."""
    project_id: int = Field(
        ...,
        alias="projectId",
        description="Project Id we sent for compile"
    )
    compile_id: str = Field(
        ...,
        alias="compileId",
        description="Compile Id for the project to backtest"
    )
    backtest_name: Optional[str] = Field(
        None,
        alias="backtestName",
        description="Optional. Name for the new backtest"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional. Parameters used in the backtest"
    )

    class Config:
        allow_population_by_field_name = True


# ============== ENUM MODELS ==============

class BacktestStatus(str, Enum):
    """Status of the backtest."""
    COMPLETED = "Completed."
    IN_QUEUE = "In Queue..."
    IN_PROGRESS = "In Progress..."
    RUNTIME_ERROR = "Runtime Error"
    RUNNING = "Running: _%" # this was from docs, but haven't seen this


# docs say it should have been this
class TradeDirection(str, Enum):
    """Direction of a trade."""
    LONG = "Long"
    SHORT = "Short"


# ============== CORE DATA MODELS ==============

class Symbol(BaseModel):
    """Represents a unique security identifier."""
    value: str = Field(..., description="The current symbol for this ticker")
    id: str = Field(..., description="The security identifier for this symbol")
    permtick: str = Field(..., description="The current symbol for this ticker")


class ResearchGuide(BaseModel):
    """A power gauge for backtests, time and parameters to estimate the overfitting risk."""
    minutes: int = Field(..., description="Number of minutes used in developing the current backtest")
    backtest_count: int = Field(
        ...,
        alias="backtestCount",
        description="The quantity of backtests run in the project"
    )
    parameters: int = Field(..., description="Number of parameters detected")

    class Config:
        allow_population_by_field_name = True


class ChartSummary(BaseModel):
    """Contains the names of all charts."""
    name: str = Field(..., description="Name of the Chart")


class ParameterSet(BaseModel):
    """Parameter set."""
    name: str = Field(..., description="Name of parameter")
    value: float = Field(..., description="Value of parameter")


class RuntimeStatistics(BaseModel):
    """Runtime banner/updating statistics."""
    equity: Optional[str] = Field(None, alias="Equity", description="Total portfolio value")
    fees: Optional[str] = Field(None, alias="Fees", description="Transaction fee")
    holdings: Optional[str] = Field(None, alias="Holdings", description="Equity value of security holdings")
    net_profit: Optional[str] = Field(None, alias="Net Profit", description="Net profit")
    probabilistic_sharpe_ratio: Optional[str] = Field(
        None,
        alias="Probabilistic Sharpe Ratio",
        description="Probabilistic Sharpe Ratio"
    )
    return_: Optional[str] = Field(None, alias="Return", description="Return")
    unrealized: Optional[str] = Field(None, alias="Unrealized", description="Unrealized profit/loss")
    volume: Optional[str] = Field(None, alias="Volume", description="Total transaction volume")

    class Config:
        allow_population_by_field_name = True


class StatisticsResult(BaseModel):
    """Statistics information sent during the algorithm operations."""
    total_orders: Optional[str] = Field(None, alias="Total Orders", description="Total number of orders")
    average_win: Optional[str] = Field(None, alias="Average Win", description="The average rate of return for winning trades")
    average_loss: Optional[str] = Field(None, alias="Average Loss", description="The average rate of return for losing trades")
    compounding_annual_return: Optional[str] = Field(
        None,
        alias="Compounding Annual Return",
        description="Annual compounded returns statistic"
    )
    drawdown: Optional[str] = Field(None, alias="Drawdown", description="Drawdown maximum percentage")
    expectancy: Optional[str] = Field(None, alias="Expectancy", description="The expected value of the rate of return")
    start_equity: Optional[str] = Field(None, alias="Start Equity", description="Initial Equity Total Value")
    end_equity: Optional[str] = Field(None, alias="End Equity", description="Final Equity Total Value")
    net_profit: Optional[str] = Field(None, alias="Net Profit", description="The total net profit percentage")
    sharpe_ratio: Optional[str] = Field(None, alias="Sharpe Ratio", description="Sharpe ratio")
    sortino_ratio: Optional[str] = Field(None, alias="Sortino Ratio", description="Sortino ratio")
    probabilistic_sharpe_ratio: Optional[str] = Field(
        None,
        alias="Probabilistic Sharpe Ratio",
        description="Probabilistic Sharpe ratio"
    )
    loss_rate: Optional[str] = Field(None, alias="Loss Rate", description="Ratio of losing trades to total trades")
    win_rate: Optional[str] = Field(None, alias="Win Rate", description="Ratio of winning trades to total trades")
    profit_loss_ratio: Optional[str] = Field(
        None,
        alias="Profit-Loss Ratio",
        description="Ratio of average win rate to average loss rate"
    )
    alpha: Optional[str] = Field(None, alias="Alpha", description="Algorithm Alpha statistic")
    beta: Optional[str] = Field(None, alias="Beta", description="Algorithm beta statistic")
    annual_standard_deviation: Optional[str] = Field(
        None,
        alias="Annual Standard Deviation",
        description="Annualized standard deviation"
    )
    annual_variance: Optional[str] = Field(
        None,
        alias="Annual Variance",
        description="Annualized variance statistic"
    )
    information_ratio: Optional[str] = Field(
        None,
        alias="Information Ratio",
        description="Information ratio - risk adjusted return"
    )
    tracking_error: Optional[str] = Field(None, alias="Tracking Error", description="Tracking error volatility")
    treynor_ratio: Optional[str] = Field(None, alias="Treynor Ratio", description="Treynor ratio statistic")
    total_fees: Optional[str] = Field(None, alias="Total Fees", description="Total amount of fees")
    estimated_strategy_capacity: Optional[str] = Field(
        None,
        alias="Estimated Strategy Capacity",
        description="Estimated total capacity of the strategy"
    )
    lowest_capacity_asset: Optional[str] = Field(
        None,
        alias="Lowest Capacity Asset",
        description="Reference to the lowest capacity symbol"
    )
    portfolio_turnover: Optional[str] = Field(
        None,
        alias="Portfolio Turnover",
        description="The average Portfolio Turnover"
    )

    class Config:
        allow_population_by_field_name = True


class TradeStatistics(BaseModel):
    """A set of statistics calculated from a list of closed trades."""

    # model_config = ConfigDict(
    #     # Handle timezone-aware datetime strings
    #     json_encoders={
    #         datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ')
    #     },
    #     populate_by_name = True
    # )

    start_date_time: datetime | None = Field(
        None,
        alias="startDateTime",
        description="The entry date/time of the first trade"
    )
    end_date_time: datetime | None = Field(
        None,
        alias="endDateTime",
        description="The exit date/time of the first trade"
    )
    total_number_of_trades: int = Field(
        ...,
        alias="totalNumberOfTrades",
        description="The total number of trades"
    )
    number_of_winning_trades: int = Field(
        ...,
        alias="numberOfWinningTrades",
        description="The total number of winning trades"
    )
    number_of_losing_trades: int = Field(
        ...,
        alias="numberOfLosingTrades",
        description="The total number of losing trades"
    )
    total_profit_loss: float = Field(
        ...,
        alias="totalProfitLoss",
        description="The total profit/loss for all trades"
    )
    total_profit: float = Field(
        ...,
        alias="totalProfit",
        description="The total profit for all winning trades"
    )
    total_loss: float = Field(
        ...,
        alias="totalLoss",
        description="The total loss for all losing trades"
    )
    largest_profit: float = Field(
        ...,
        alias="largestProfit",
        description="The largest profit in a single trade"
    )
    largest_loss: float = Field(
        ...,
        alias="largestLoss",
        description="The largest loss in a single trade"
    )
    average_profit_loss: float = Field(
        ...,
        alias="averageProfitLoss",
        description="The average profit/loss for all trades"
    )
    average_profit: float = Field(
        ...,
        alias="averageProfit",
        description="The average profit for all winning trades"
    )
    average_loss: float = Field(
        ...,
        alias="averageLoss",
        description="The average loss for all winning trades"
    )
    average_trade_duration: str = Field(
        ...,
        alias="averageTradeDuration",
        description="The average duration for all trades"
    )
    average_winning_trade_duration: str = Field(
        ...,
        alias="averageWinningTradeDuration",
        description="The average duration for all winning trades"
    )
    average_losing_trade_duration: str = Field(
        ...,
        alias="averageLosingTradeDuration",
        description="The average duration for all losing trades"
    )
    median_trade_duration: str = Field(
        ...,
        alias="medianTradeDuration",
        description="The median duration for all trades"
    )
    median_winning_trade_duration: str = Field(
        ...,
        alias="medianWinningTradeDuration",
        description="The median duration for all winning trades"
    )
    median_losing_trade_duration: str = Field(
        ...,
        alias="medianLosingTradeDuration",
        description="The median duration for all losing trades"
    )
    max_consecutive_winning_trades: int = Field(
        ...,
        alias="maxConsecutiveWinningTrades",
        description="The maximum number of consecutive winning trades"
    )
    max_consecutive_losing_trades: int = Field(
        ...,
        alias="maxConsecutiveLosingTrades",
        description="The maximum number of consecutive losing trades"
    )
    profit_loss_ratio: float = Field(
        ...,
        alias="profitLossRatio",
        description="The ratio of the average profit per trade to the average loss per trade"
    )
    win_loss_ratio: float = Field(
        ...,
        alias="winLossRatio",
        description="The ratio of the number of winning trades to the number of losing trades"
    )
    win_rate: float = Field(
        ...,
        alias="winRate",
        description="The ratio of the number of winning trades to the total number of trades"
    )
    loss_rate: float = Field(
        ...,
        alias="lossRate",
        description="The ratio of the number of losing trades to the total number of trades"
    )
    average_mae: float = Field(
        ...,
        alias="averageMAE",
        description="The average Maximum Adverse Excursion for all trades"
    )
    average_mfe: float = Field(
        ...,
        alias="averageMFE",
        description="The average Maximum Adverse Excursion for all trades"
    )
    largest_mae: float = Field(
        ...,
        alias="largestMAE",
        description="The average Maximum Favorable Excursion for all trades"
    )
    largest_mfe: float = Field(
        ...,
        alias="largestMFE",
        description="The largest Maximum Adverse Excursion in a single trade"
    )
    maximum_closed_trade_drawdown: float = Field(
        ...,
        alias="maximumClosedTradeDrawdown",
        description="The maximum closed-trade drawdown for all trades"
    )
    maximum_intra_trade_drawdown: float = Field(
        ...,
        alias="maximumIntraTradeDrawdown",
        description="The maximum intra-trade drawdown for all trades"
    )
    profit_loss_standard_deviation: float = Field(
        ...,
        alias="profitLossStandardDeviation",
        description="The standard deviation of the profits/losses for all trades"
    )
    profit_loss_downside_deviation: float = Field(
        ...,
        alias="profitLossDownsideDeviation",
        description="The downside deviation of the profits/losses for all trades"
    )
    profit_factor: float = Field(
        ...,
        alias="profitFactor",
        description="The ratio of the total profit to the total loss"
    )
    sharpe_ratio: float = Field(
        ...,
        alias="sharpeRatio",
        description="The ratio of the average profit/loss to the standard deviation"
    )
    sortino_ratio: float = Field(
        ...,
        alias="sortinoRatio",
        description="The ratio of the average profit/loss to the downside deviation"
    )
    profit_to_max_drawdown_ratio: float = Field(
        ...,
        alias="profitToMaxDrawdownRatio",
        description="The ratio of the total profit/loss to the maximum closed trade drawdown"
    )
    maximum_end_trade_drawdown: float = Field(
        ...,
        alias="maximumEndTradeDrawdown",
        description="The maximum amount of profit given back by a single trade before exit"
    )
    average_end_trade_drawdown: float = Field(
        ...,
        alias="averageEndTradeDrawdown",
        description="The average amount of profit given back by all trades before exit"
    )
    maximum_drawdown_duration: str = Field(
        ...,
        alias="maximumDrawdownDuration",
        description="The maximum amount of time to recover from a drawdown"
    )
    total_fees: float = Field(
        ...,
        alias="totalFees",
        description="The sum of fees for all trades"
    )



class PortfolioStatistics(BaseModel):
    """Represents a set of statistics calculated from equity and benchmark samples."""
    average_win_rate: float = Field(
        ...,
        alias="averageWinRate",
        description="The average rate of return for winning trades"
    )
    average_loss_rate: float = Field(
        ...,
        alias="averageLossRate",
        description="The average rate of return for losing trades"
    )
    profit_loss_ratio: float = Field(
        ...,
        alias="profitLossRatio",
        description="The ratio of the average win rate to the average loss rate"
    )
    win_rate: float = Field(
        ...,
        alias="winRate",
        description="The ratio of the number of winning trades to the total number of trades"
    )
    loss_rate: float = Field(
        ...,
        alias="lossRate",
        description="The ratio of the number of losing trades to the total number of trades"
    )
    expectancy: float = Field(..., description="The expected value of the rate of return")
    start_equity: float = Field(
        ...,
        alias="startEquity",
        description="Initial Equity Total Value"
    )
    end_equity: float = Field(
        ...,
        alias="endEquity",
        description="Final Equity Total Value"
    )
    compounding_annual_return: float = Field(
        ...,
        alias="compoundingAnnualReturn",
        description="Annual compounded returns statistic"
    )
    drawdown: float = Field(..., description="Drawdown maximum percentage")
    total_net_profit: float = Field(
        ...,
        alias="totalNetProfit",
        description="The total net profit percentage"
    )
    sharpe_ratio: float = Field(
        ...,
        alias="sharpeRatio",
        description="Sharpe ratio with respect to risk free rate"
    )
    probabilistic_sharpe_ratio: float = Field(
        ...,
        alias="probabilisticSharpeRatio",
        description="Probabilistic Sharpe Ratio"
    )
    sortino_ratio: float = Field(
        ...,
        alias="sortinoRatio",
        description="Sortino ratio with respect to risk free rate"
    )
    alpha: float = Field(..., description="Algorithm Alpha statistic")
    beta: float = Field(..., description="Algorithm beta statistic")
    annual_standard_deviation: float = Field(
        ...,
        alias="annualStandardDeviation",
        description="Annualized standard deviation"
    )
    annual_variance: float = Field(
        ...,
        alias="annualVariance",
        description="Annualized variance statistic"
    )
    information_ratio: float = Field(
        ...,
        alias="informationRatio",
        description="Information ratio - risk adjusted return"
    )
    tracking_error: float = Field(
        ...,
        alias="trackingError",
        description="Tracking error volatility"
    )
    treynor_ratio: float = Field(
        ...,
        alias="treynorRatio",
        description="Treynor ratio statistic"
    )
    portfolio_turnover: float = Field(
        ...,
        alias="portfolioTurnover",
        description="The average Portfolio Turnover"
    )
    value_at_risk_99: float = Field(
        ...,
        alias="valueAtRisk99",
        description="The 1-day VaR for the portfolio, 99% confidence level"
    )
    value_at_risk_95: float = Field(
        ...,
        alias="valueAtRisk95",
        description="The 1-day VaR for the portfolio, 95% confidence level"
    )

    class Config:
        allow_population_by_field_name = True


class Trade(BaseModel):
    """Represents a closed trade."""
    symbol: Symbol = Field(..., description="Represents a unique security identifier")
    entry_time: datetime = Field(
        ...,
        alias="entryTime",
        description="The date and time the trade was opened"
    )
    entry_price: float = Field(
        ...,
        alias="entryPrice",
        description="The price at which the trade was opened"
    )
    # Docs say it should have been this
    # direction: TradeDirection = Field(..., description="Direction of a trade")
    direction: int = Field(..., description="Direction of a trade")
    quantity: float = Field(..., description="The total unsigned quantity of the trade")
    exit_time: datetime = Field(
        ...,
        alias="exitTime",
        description="The date and time the trade was closed"
    )
    exit_price: float = Field(
        ...,
        alias="exitPrice",
        description="The price at which the trade was closed"
    )
    profit_loss: float = Field(
        ...,
        alias="profitLoss",
        description="The gross profit/loss of the trade"
    )
    total_fees: float = Field(
        ...,
        alias="totalFees",
        description="The total fees associated with the trade"
    )
    mae: float = Field(..., description="The Maximum Adverse Excursion")
    mfe: float = Field(..., description="The Maximum Favorable Excursion")
    duration: str = Field(..., description="The duration of the trade")
    end_trade_drawdown: float = Field(
        ...,
        alias="endTradeDrawdown",
        description="The amount of profit given back before the trade was closed"
    )

    class Config:
        allow_population_by_field_name = True


class AlgorithmPerformance(BaseModel):
    """The AlgorithmPerformance class is a wrapper for TradeStatistics and PortfolioStatistics."""
    trade_statistics: TradeStatistics = Field(
        ...,
        alias="tradeStatistics",
        description="A set of statistics calculated from a list of closed trades"
    )
    portfolio_statistics: PortfolioStatistics = Field(
        ...,
        alias="portfolioStatistics",
        description="Represents a set of statistics calculated from equity and benchmark samples"
    )
    closed_trades: List[Trade] = Field(
        ...,
        alias="closedTrades",
        description="The algorithm statistics on portfolio"
    )

    class Config:
        allow_population_by_field_name = True


class BacktestResult(BaseModel):
    """Results object class. Results are exhaust from backtest or live algorithms running in LEAN."""
    note: None | str = Field(None, description="Note on the backtest attached by the user")
    name: str = Field(..., description="Name of the backtest")
    organization_id: str = Field(
        ...,
        alias="organizationId",
        description="Organization ID"
    )
    project_id: int = Field(
        ...,
        alias="projectId",
        description="Project ID"
    )
    completed: bool = Field(..., description="Boolean true when the backtest is completed")
    optimization_id: Optional[str] = Field(
        None,
        alias="optimizationId",
        description="Optimization task ID, if the backtest is part of an optimization"
    )
    backtest_id: str = Field(
        ...,
        alias="backtestId",
        description="Assigned backtest ID"
    )
    tradeable_dates: int = Field(
        ...,
        alias="tradeableDates",
        description="Number of tradeable days"
    )
    research_guide: ResearchGuide = Field(
        ...,
        alias="researchGuide",
        description="A power gauge for backtests"
    )
    backtest_start: datetime = Field(
        ...,
        alias="backtestStart",
        description="The starting time of the backtest"
    )
    backtest_end: datetime = Field(
        ...,
        alias="backtestEnd",
        description="The ending time of the backtest"
    )
    created: datetime = Field(..., description="Backtest creation date and time")
    snapshot_id: int = Field(
        ...,
        alias="snapshotId",
        description="Snapshot id of this backtest result"
    )
    status: BacktestStatus = Field(..., description="Status of the backtest")
    error: Optional[str] = Field(None, description="Backtest error message")
    stacktrace: Optional[str] = Field(None, description="Backtest error stacktrace")
    progress: float = Field(
        ...,
        description="Progress of the backtest in percent 0-1",
        ge=0.0,
        le=1.0
    )
    has_initialize_error: bool = Field(
        ...,
        alias="hasInitializeError",
        description="Indicates if the backtest has error during initialization"
    )
    charts: dict[str, ChartSummary] = Field(
        ...,
        description="Charts updates for the live algorithm"
    )
    parameter_set: dict = Field(
        ...,
        alias="parameterSet",
        description="Parameters used in the backtest"
    )
    rolling_window: dict[str, AlgorithmPerformance] | None = Field(
        None,
        alias="rollingWindow",
        description="Rolling window detailed statistics"
    )
    runtime_statistics: RuntimeStatistics = Field(
        ...,
        alias="runtimeStatistics",
        description="Runtime banner/updating statistics"
    )
    statistics: StatisticsResult = Field(
        ...,
        description="Statistics information sent during the algorithm operations"
    )
    total_performance: AlgorithmPerformance | None= Field(
        None,
        alias="totalPerformance",
        description="The algorithm performance statistics"
    )
    node_name: str = Field(
        ...,
        alias="nodeName",
        description="The backtest node name"
    )
    out_of_sample_max_end_date: Optional[datetime] = Field(
        None,
        alias="outOfSampleMaxEndDate",
        description="End date of out of sample data"
    )
    out_of_sample_days: int | None = Field(
        None, 
        alias="outOfSampleDays",
        description="Number of days of out of sample days"
    )

    class Config:
        allow_population_by_field_name = True


# ============== RESPONSE MODELS ==============

class BacktestResponse(BaseModel):
    """Collection container for a list of backtests for a project."""
    backtest: BacktestResult = Field(
        ...,
        description="Collection of backtests for a project"
    )
    debugging: bool | None = Field(
        None,
        description="Indicates if the backtest is run under debugging mode"
    )
    success: bool = Field(
        ...,
        description="Indicate if the API request was successful"
    )
    errors: Optional[List[str]] = Field(
        None,
        description="List of errors with the API call"
    )


class UnauthorizedError(BaseModel):
    """Unauthorized response from the API."""
    www_authenticate: str = Field(
        ...,
        alias="www_authenticate",
        description="Header"
    )

    class Config:
        allow_population_by_field_name = True


# ============== EXAMPLE USAGE ==============

if __name__ == "__main__":
    # Example request
    create_request = CreateBacktestRequest(
        projectId=23456789,
        compileId="c0edc6-49048b",
        backtestName="New Backtest",
        parameters={"ema_fast": 10, "ema_slow": 100}
    )
    
    print("Create Request JSON:")
    print(create_request.json(indent=2))
    
    # Example response parsing
    sample_response_data = {
        "backtest": [],
        "debugging": True,
        "success": True,
        "errors": None
    }
    
    response = BacktestResponse(**sample_response_data)
    print(f"\nResponse Success: {response.success}")
    print(f"Debugging Mode: {response.debugging}")
