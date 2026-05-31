import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse

from strategies.mean_reversion_strategy import MeanReversionStrategy
from utils.logger import logger

class DemoBacktester:
    """Demo backtester with sample data - no API needed"""
    
    def __init__(self, symbol: str, initial_balance: float = 1000):
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.strategy = MeanReversionStrategy(symbol)
        
        self.trades = []
        self.closed_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0
        self.max_drawdown = 0
        self.peak_balance = initial_balance
    
    def generate_sample_data(self, num_candles: int = 500) -> list:
        """Generate realistic sample OHLCV data for demo"""
        candles = []
        price = 45000  # BTC starting price
        
        for i in range(num_candles):
            # Simulate random walk with mean reversion
            change = np.random.normal(0, 300)  # Random movement
            if price > 48000:
                change -= 200  # Mean reversion down
            elif price < 42000:
                change += 200  # Mean reversion up
            
            price += change
            
            # Generate OHLCV
            open_price = price
            high = price + abs(np.random.normal(0, 150))
            low = price - abs(np.random.normal(0, 150))
            close = np.random.uniform(low, high)
            volume = np.random.uniform(10, 100)
            
            timestamp = datetime(2024, 1, 1) + timedelta(minutes=15*i)
            
            candles.append({
                "timestamp": int(timestamp.timestamp() * 1000),
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close, 2),
                "volume": round(volume, 2)
            })
        
        return candles
    
    def simulate_trade(self, candles: list, index: int) -> dict:
        """Simulate a single trade"""
        
        if index < 50:
            return None
        
        current_candles = candles[:index+1]
        signal = self.strategy.analyze(current_candles)
        
        if not signal.get("confirmed"):
            return None
        
        entry_price = candles[index]["close"]
        stop_loss = signal["stop_loss"]
        take_profit = signal["take_profit"]
        side = "buy" if signal["buy"] else "sell"
        
        risk_amount = self.current_balance * 0.02
        price_diff = abs(entry_price - stop_loss)
        
        if price_diff == 0:
            return None
        
        position_size = risk_amount / price_diff
        trade_result = self.simulate_exit(candles, index, entry_price, stop_loss, take_profit, side)
        
        if trade_result:
            return {
                "entry_price": round(entry_price, 2),
                "exit_price": round(trade_result["exit_price"], 2),
                "side": side,
                "position_size": round(position_size, 4),
                "pnl": round(trade_result["pnl"], 2),
                "reason": trade_result["reason"],
                "rr": round(signal["rr"], 2)
            }
        
        return None
    
    def simulate_exit(self, candles: list, entry_index: int, 
                     entry_price: float, stop_loss: float, take_profit: float, side: str) -> dict:
        """Simulate trade exit"""
        
        for i in range(entry_index + 1, min(entry_index + 100, len(candles))):
            candle = candles[i]
            high = candle["high"]
            low = candle["low"]
            
            if side == "buy":
                if high >= take_profit:
                    pnl = (take_profit - entry_price) * 100
                    return {"exit_price": take_profit, "pnl": pnl, "reason": "TP"}
                if low <= stop_loss:
                    pnl = (stop_loss - entry_price) * 100
                    return {"exit_price": stop_loss, "pnl": pnl, "reason": "SL"}
            else:
                if low <= take_profit:
                    pnl = (entry_price - take_profit) * 100
                    return {"exit_price": take_profit, "pnl": pnl, "reason": "TP"}
                if high >= stop_loss:
                    pnl = (entry_price - stop_loss) * 100
                    return {"exit_price": stop_loss, "pnl": pnl, "reason": "SL"}
        
        return None
    
    def run_backtest(self):
        """Run demo backtest with sample data"""
        
        logger.info(f"Starting DEMO backtest for {self.symbol}")
        candles = self.generate_sample_data(500)
        
        logger.info(f"Generated {len(candles)} sample candles")
        
        for i in range(len(candles)):
            trade = self.simulate_trade(candles, i)
            
            if trade:
                self.trades.append(trade)
                self.closed_trades += 1
                self.current_balance += trade["pnl"]
                self.total_pnl += trade["pnl"]
                
                if trade["pnl"] > 0:
                    self.winning_trades += 1
                else:
                    self.losing_trades += 1
                
                if self.current_balance > self.peak_balance:
                    self.peak_balance = self.current_balance
                
                drawdown = ((self.peak_balance - self.current_balance) / self.peak_balance) * 100
                self.max_drawdown = max(self.max_drawdown, drawdown)
        
        self.print_results()
    
    def print_results(self):
        """Print backtest results"""
        
        win_rate = (self.winning_trades / self.closed_trades * 100) if self.closed_trades > 0 else 0
        avg_win = np.mean([t["pnl"] for t in self.trades if t["pnl"] > 0]) if self.winning_trades > 0 else 0
        avg_loss = np.mean([t["pnl"] for t in self.trades if t["pnl"] < 0]) if self.losing_trades > 0 else 0
        profit_factor = abs(sum([t["pnl"] for t in self.trades if t["pnl"] > 0]) / sum([t["pnl"] for t in self.trades if t["pnl"] < 0])) if self.losing_trades > 0 else 0
        
        print("\n" + "="*70)
        print("DEMO BACKTEST RESULTS - Mean Reversion Strategy")
        print("="*70)
        print(f"Symbol: {self.symbol}")
        print(f"Initial Balance: ${self.initial_balance:,.2f}")
        print(f"Final Balance: ${self.current_balance:,.2f}")
        print(f"Total PnL: ${self.total_pnl:,.2f}")
        print(f"ROI: {(self.total_pnl / self.initial_balance * 100):.2f}%")
        print(f"\n--- Trade Statistics ---")
        print(f"Total Trades: {self.closed_trades}")
        print(f"Winning Trades: {self.winning_trades}")
        print(f"Losing Trades: {self.losing_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Profit Factor: {profit_factor:.2f}")
        print(f"\n--- Performance Metrics ---")
        print(f"Average Win: ${avg_win:,.2f}")
        print(f"Average Loss: ${avg_loss:,.2f}")
        print(f"Max Drawdown: {self.max_drawdown:.2f}%")
        print(f"Avg RR Ratio: {np.mean([t['rr'] for t in self.trades]):.2f}:1")
        print("="*70)
        
        if self.closed_trades > 0:
            print(f"\n--- Recent Trades ---")
            for i, trade in enumerate(self.trades[-5:], 1):
                status = "✅ WIN" if trade["pnl"] > 0 else "❌ LOSS"
                print(f"{i}. {trade['side'].upper():4s} @ ${trade['entry_price']:,.0f} → ${trade['exit_price']:,.0f} | PnL: ${trade['pnl']:>7.2f} | {status}")

def main():
    parser = argparse.ArgumentParser(description="Demo backtest with sample data")
    parser.add_argument("--symbol", default="BTC_USDT", help="Trading symbol")
    parser.add_argument("--balance", type=float, default=1000, help="Initial balance")
    
    args = parser.parse_args()
    
    backtester = DemoBacktester(args.symbol, args.balance)
    backtester.run_backtest()

if __name__ == "__main__":
    main()
