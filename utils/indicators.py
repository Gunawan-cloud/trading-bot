import numpy as np
import pandas as pd
from config.settings import settings

class TechnicalIndicators:
    @staticmethod
    def rsi(data: np.ndarray, period: int = 14) -> np.ndarray:
        if len(data) < period:
            return np.full(len(data), 50)
        deltas = np.diff(data)
        seed = deltas[:period + 1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(data)
        rsi[:period] = 100 - (100 / (1 + rs))
        for i in range(period, len(data)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0
            else:
                upval = 0
                downval = -delta
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down if down != 0 else 0
            rsi[i] = 100 - (100 / (1 + rs))
        return rsi
    @staticmethod
    def macd(data: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        ema_fast = pd.Series(data).ewm(span=fast).mean().values
        ema_slow = pd.Series(data).ewm(span=slow).mean().values
        macd_line = ema_fast - ema_slow
        signal_line = pd.Series(macd_line).ewm(span=signal).mean().values
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    @staticmethod
    def bollinger_bands(data: np.ndarray, period: int = 20, std_dev: float = 2.0) -> tuple:
        sma = pd.Series(data).rolling(window=period).mean().values
        std = pd.Series(data).rolling(window=period).std().values
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    @staticmethod
    def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        tr = np.maximum(tr1, tr2)
        tr = np.maximum(tr, tr3)
        atr = pd.Series(tr).rolling(window=period).mean().values
        return atr

class SignalGenerator:
    @staticmethod
    def mean_reversion_signal(close: np.ndarray, rsi: np.ndarray, upper_bb: np.ndarray, lower_bb: np.ndarray) -> dict:
        current_price = close[-1]
        current_rsi = rsi[-1]
        signal = {"buy": False, "sell": False, "strength": 0}
        if current_rsi < settings.RSI_OVERSOLD and current_price < lower_bb[-1]:
            signal["buy"] = True
            signal["strength"] = min(100, (settings.RSI_OVERSOLD - current_rsi) * 3)
        elif current_rsi > settings.RSI_OVERBOUGHT and current_price > upper_bb[-1]:
            signal["sell"] = True
            signal["strength"] = min(100, (current_rsi - settings.RSI_OVERBOUGHT) * 3)
        return signal
    @staticmethod
    def macd_signal(macd_line: np.ndarray, signal_line: np.ndarray) -> dict:
        signal = {"buy": False, "sell": False}
        if len(macd_line) < 2:
            return signal
        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            signal["buy"] = True
        elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            signal["sell"] = True
        return signal