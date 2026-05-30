import ccxt
import time
from typing import Dict, List, Optional
from config.settings import settings
from utils.logger import logger

class GateIOClient:
    def __init__(self):
        self.exchange = ccxt.gateio({'apiKey': settings.GATEIO_API_KEY, 'secret': settings.GATEIO_API_SECRET, 'uid': settings.GATEIO_UID, 'enableRateLimit': True})
        self.session_trades = 0
        self.session_pnl = 0
    def get_balance(self) -> Dict:
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return None
    def get_candles(self, symbol: str, timeframe: str = '15m', limit: int = 100) -> List[Dict]:
        try:
            candles = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            formatted_candles = []
            for candle in candles:
                formatted_candles.append({"timestamp": candle[0], "open": candle[1], "high": candle[2], "low": candle[3], "close": candle[4], "volume": candle[5]})
            return formatted_candles
        except Exception as e:
            logger.error(f"Error fetching candles for {symbol}: {e}")
            return []
    def create_order(self, symbol: str, order_type: str, side: str, amount: float, price: float = None, params: Dict = None) -> Dict:
        try:
            if params is None:
                params = {}
            order = self.exchange.create_order(symbol, order_type, side, amount, price, params)
            logger.info(f"Order created: {order}")
            return order
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    def create_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        return self.create_order(symbol, 'market', side, amount)
    def create_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
        return self.create_order(symbol, 'limit', side, amount, price)
    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        except Exception as e:
            logger.error(f"Error fetching open orders: {e}")
            return []
    def get_ticker(self, symbol: str) -> Dict:
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {"bid": ticker['bid'], "ask": ticker['ask'], "last": ticker['last'], "high": ticker['high'], "low": ticker['low'], "volume": ticker['quoteVolume']}
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            return None