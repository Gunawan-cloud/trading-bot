import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import argparse

from exchanges.gateio_client import GateIOClient
from strategies.mean_reversion_strategy import MeanReversionStrategy
from utils.logger import logger

class Backtester:
    def __init__(self, symbol: str, initial_balance: float = 1000):
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.exchange = GateIOClient()
        self.strategy = MeanReversionStrategy(symbol)
        self.trades = []
        self.closed_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0
        self.max_drawdown = 0
        self.peak_balance = initial_balance
    def run_backtest(self, start_date: str, end_date: str):
        logger.info(f"Starting backtest for {self.symbol}")
        print(f"\nBacktest Mode: {self.symbol}")
        print(f"Initial Balance: ${self.initial_balance}")
        print(f"Strategy: Mean Reversion (70-80% win rate)")
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Backtest trading strategy")
    parser.add_argument("--symbol", default="BTC_USDT", help="Trading symbol")
    parser.add_argument("--start", default="2024-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default="2024-12-31", help="End date YYYY-MM-DD")
    parser.add_argument("--balance", type=float, default=1000, help="Initial balance")
    args = parser.parse_args()
    backtester = Backtester(args.symbol, args.balance)
    backtester.run_backtest(args.start, args.end)

if __name__ == "__main__":
    main()