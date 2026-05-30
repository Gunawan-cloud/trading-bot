from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, List, Optional
from config.settings import settings
from utils.logger import logger

class BaseStrategy(ABC):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.last_signal = None
        self.position_open = False
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
    @abstractmethod
    def analyze(self, candles: List[Dict]) -> Dict:
        pass
    def validate_signal(self, signal: Dict) -> bool:
        if not signal:
            return False
        if signal.get("strength", 0) < 50:
            return False
        if not signal.get("confirmed", False):
            return False
        return True
    def reset(self):
        self.last_signal = None
        self.position_open = False
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0