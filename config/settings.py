import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    GATEIO_API_KEY: str = os.getenv("GATEIO_API_KEY", "")
    GATEIO_API_SECRET: str = os.getenv("GATEIO_API_SECRET", "")
    GATEIO_UID: str = os.getenv("GATEIO_UID", "")
    TRADING_SYMBOLS: list = os.getenv("TRADING_SYMBOLS", "BTC_USDT,ETH_USDT").split(",")
    RISK_PER_TRADE: float = float(os.getenv("RISK_PER_TRADE", "2.0"))
    MAX_POSITION_SIZE: float = float(os.getenv("MAX_POSITION_SIZE", "100"))
    MAX_DAILY_LOSS: float = float(os.getenv("MAX_DAILY_LOSS", "500"))
    MAX_OPEN_POSITIONS: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    RSI_PERIOD: int = int(os.getenv("RSI_PERIOD", "14"))
    RSI_OVERSOLD: int = int(os.getenv("RSI_OVERSOLD", "30"))
    RSI_OVERBOUGHT: int = int(os.getenv("RSI_OVERBOUGHT", "70"))
    MACD_FAST: int = int(os.getenv("MACD_FAST", "12"))
    MACD_SLOW: int = int(os.getenv("MACD_SLOW", "26"))
    MACD_SIGNAL: int = int(os.getenv("MACD_SIGNAL", "9"))
    BB_PERIOD: int = int(os.getenv("BB_PERIOD", "20"))
    MODE: str = os.getenv("MODE", "backtest")
    LEVERAGE: int = int(os.getenv("LEVERAGE", "10"))
    POSITION_TYPE: str = os.getenv("POSITION_TYPE", "long")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/trading_bot.log")
    ENABLE_TELEGRAM: bool = os.getenv("ENABLE_TELEGRAM", "false").lower() == "true"
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    class Config:
        case_sensitive = True

settings = Settings()
