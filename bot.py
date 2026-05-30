#!/usr/bin/env python3
"""
Main Trading Bot - GateIO Mean Reversion Strategy
Target: 70-80% win rate
"""

import time
import signal
from datetime import datetime
from config.settings import settings
from exchanges.gateio_client import GateIOClient
from strategies.mean_reversion_strategy import MeanReversionStrategy
from utils.logger import logger
from utils.risk_manager import RiskManager

class TradingBot:
    def __init__(self):
        self.exchange = GateIOClient()
        self.strategies = {}
        self.risk_manager = RiskManager()
        self.running = True
        self.session_trades = 0
        self.session_pnl = 0
        for symbol in settings.TRADING_SYMBOLS:
            self.strategies[symbol] = MeanReversionStrategy(symbol)
        logger.info(f"Trading bot initialized for symbols: {settings.TRADING_SYMBOLS}")
    def run(self):
        logger.info("Starting trading bot...")
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        while self.running:
            try:
                self.scan_and_trade()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)
    def scan_and_trade(self):
        balance = self.exchange.get_balance()
        if not balance:
            logger.error("Failed to get balance")
            return
        account_balance = balance.get('USDT', {}).get('free', 0)
        logger.debug(f"Account Balance: ${account_balance:.2f}")
        for symbol in settings.TRADING_SYMBOLS:
            try:
                self.process_symbol(symbol, account_balance)
            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")
    def process_symbol(self, symbol: str, account_balance: float):
        candles = self.exchange.get_candles(symbol, '15m', limit=100)
        if not candles or len(candles) < 50:
            logger.warning(f"Not enough candles for {symbol}")
            return
        strategy = self.strategies[symbol]
        signal_data = strategy.analyze(candles)
        if not signal_data.get("confirmed"):
            return
        if not self.risk_manager.can_open_position():
            logger.warning(f"Cannot open position for {symbol}")
            return
        logger.info(f"New signal for {symbol}: {signal_data}")
    def shutdown(self, sig, frame):
        logger.info("Shutdown signal received")
        self.running = False
        logger.info(f"\nSession Stats:")
        logger.info(f"Trades: {self.session_trades}")
        logger.info(f"Session PnL: ${self.session_pnl:.2f}")
        logger.info(f"Win Rate: {self.risk_manager.calculate_win_rate():.2f}%")
        exit(0)

def main():
    if settings.MODE == "backtest":
        logger.info("Running in backtest mode")
        from backtest.backtester import Backtester
        backtester = Backtester(settings.TRADING_SYMBOLS[0], 1000)
        backtester.run_backtest("2024-01-01", "2024-12-31")
    else:
        logger.info("Running in live mode")
        bot = TradingBot()
        bot.run()

if __name__ == "__main__":
    main()