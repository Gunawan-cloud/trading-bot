import numpy as np
from typing import Dict, List
from strategies.base_strategy import BaseStrategy
from utils.indicators import TechnicalIndicators, SignalGenerator
from utils.risk_manager import RiskManager
from config.settings import settings
from utils.logger import logger

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.risk_manager = RiskManager()
        self.last_rsi = 50
    def analyze(self, candles: List[Dict]) -> Dict:
        if len(candles) < 50:
            return {"buy": False, "sell": False, "strength": 0}
        close = np.array([c["close"] for c in candles])
        high = np.array([c["high"] for c in candles])
        low = np.array([c["low"] for c in candles])
        rsi = TechnicalIndicators.rsi(close, settings.RSI_PERIOD)
        upper_bb, sma, lower_bb = TechnicalIndicators.bollinger_bands(close, settings.BB_PERIOD)
        macd_line, signal_line, histogram = TechnicalIndicators.macd(close, settings.MACD_FAST, settings.MACD_SLOW, settings.MACD_SIGNAL)
        atr = TechnicalIndicators.atr(high, low, close, 14)
        current_price = close[-1]
        current_rsi = rsi[-1]
        current_atr = atr[-1]
        signal = {"buy": False, "sell": False, "strength": 0, "confirmed": False, "stop_loss": 0, "take_profit": 0, "rr": 0}
        mr_signal = SignalGenerator.mean_reversion_signal(close, rsi, upper_bb, lower_bb)
        macd_signal = SignalGenerator.macd_signal(macd_line, signal_line)
        if (mr_signal["buy"] and current_rsi < settings.RSI_OVERSOLD and current_price < lower_bb[-1]):
            if (macd_signal.get("buy") or (len(histogram) >= 2 and histogram[-1] > histogram[-2])):
                signal["buy"] = True
                signal["confirmed"] = True
                signal["strength"] = min(100, (settings.RSI_OVERSOLD - current_rsi) * 2)
                signal["stop_loss"] = current_price - (current_atr * 1.5)
                signal["take_profit"] = current_price + (current_atr * 3.0)
                signal["rr"] = (signal["take_profit"] - current_price) / (current_price - signal["stop_loss"])
        elif (mr_signal["sell"] and current_rsi > settings.RSI_OVERBOUGHT and current_price > upper_bb[-1]):
            if (macd_signal.get("sell") or (len(histogram) >= 2 and histogram[-1] < histogram[-2])):
                signal["sell"] = True
                signal["confirmed"] = True
                signal["strength"] = min(100, (current_rsi - settings.RSI_OVERBOUGHT) * 2)
                signal["stop_loss"] = current_price + (current_atr * 1.5)
                signal["take_profit"] = current_price - (current_atr * 3.0)
                signal["rr"] = (current_price - signal["take_profit"]) / (signal["stop_loss"] - current_price)
        self.last_signal = signal
        return signal