import numpy as np
from config.settings import settings
from utils.logger import logger

class RiskManager:
    def __init__(self):
        self.daily_loss = 0
        self.open_positions = []
        self.total_trades = 0
        self.winning_trades = 0
    def calculate_position_size(self, account_balance: float, entry_price: float, stop_loss: float, risk_percent: float = None) -> float:
        if risk_percent is None:
            risk_percent = settings.RISK_PER_TRADE
        risk_amount = account_balance * (risk_percent / 100)
        price_diff = abs(entry_price - stop_loss)
        if price_diff == 0:
            return 0
        position_size = risk_amount / price_diff
        max_size = account_balance * (settings.MAX_POSITION_SIZE / 100)
        position_size = min(position_size, max_size)
        return position_size
    def can_open_position(self) -> bool:
        if len(self.open_positions) >= settings.MAX_OPEN_POSITIONS:
            logger.warning(f"Max open positions ({settings.MAX_OPEN_POSITIONS}) reached")
            return False
        if self.daily_loss > settings.MAX_DAILY_LOSS:
            logger.warning("Daily loss limit exceeded")
            return False
        return True
    def calculate_win_rate(self) -> float:
        if self.total_trades == 0:
            return 0
        return (self.winning_trades / self.total_trades) * 100
    def update_trade_stats(self, pnl: float):
        self.total_trades += 1
        if pnl > 0:
            self.winning_trades += 1