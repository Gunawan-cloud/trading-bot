import logging
import os
from datetime import datetime
from config.settings import settings

class TradingLogger:
    def __init__(self, name: str = "TradingBot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        fh = logging.FileHandler(settings.LOG_FILE)
        fh.setLevel(getattr(logging, settings.LOG_LEVEL))
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, settings.LOG_LEVEL))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def info(self, message: str):
        self.logger.info(message)
    def error(self, message: str):
        self.logger.error(message)
    def warning(self, message: str):
        self.logger.warning(message)
    def debug(self, message: str):
        self.logger.debug(message)
    def trade(self, trade_data: dict):
        log_msg = f"TRADE | Symbol: {trade_data.get('symbol')} | Side: {trade_data.get('side')} | Price: {trade_data.get('price')} | Size: {trade_data.get('size')} | RR: {trade_data.get('rr')}R"
        self.info(log_msg)

logger = TradingLogger()