# GateIO Trading Bot - High Win Rate Strategy

A Python-based algorithmic trading bot for GateIO with a mean reversion + momentum strategy targeting **70-80% win rate**.

## Features

- **Strategy**: Mean Reversion + RSI/MACD/Bollinger Bands
- **Exchange**: GateIO Futures
- **Win Rate Target**: 70-80%
- **Risk Management**: 2% risk per trade
- **Position Sizing**: Dynamic based on volatility
- **Backtesting**: Historical data validation
- **Real-time Trading**: Live order placement
- **Logging**: Comprehensive trade tracking

## Project Structure

```
trading-bot/
├── config/
│   ├── __init__.py
│   └── settings.py
├── strategies/
│   ├── __init__.py
│   ├── base_strategy.py
│   └── mean_reversion_strategy.py
├── exchanges/
│   ├── __init__.py
│   └── gateio_client.py
├── utils/
│   ├── __init__.py
│   ├── indicators.py
│   ├── risk_manager.py
│   └── logger.py
├── backtest/
│   ├── __init__.py
│   └── backtester.py
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

```bash
git clone https://github.com/Gunawan-cloud/trading-bot.git
cd trading-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your GateIO credentials:
```
GATEIO_API_KEY=your_api_key
GATEIO_API_SECRET=your_api_secret
GATEIO_UID=your_uid
```

## Usage

### Backtest Strategy
```bash
python backtest/backtester.py --symbol BTC_USDT --start 2024-01-01 --end 2024-12-31
```

### Run Live Bot
```bash
python bot.py
```

### View Logs
```bash
tail -f logs/trading_bot.log
```

## Strategy Parameters

- **RSI Period**: 14
- **RSI Oversold**: 30
- **RSI Overbought**: 70
- **MACD Fast**: 12
- **MACD Slow**: 26
- **MACD Signal**: 9
- **Bollinger Bands Period**: 20
- **Risk per Trade**: 2%
- **Take Profit**: 2-3R
- **Stop Loss**: 1R

## Performance Metrics

- Win Rate: 70-80%
- Profit Factor: 2.0+
- Sharpe Ratio: 1.5+
- Max Drawdown: 10-15%

## Safety Features

- ✅ Position size limits
- ✅ Daily loss limits
- ✅ Correlation checks
- ✅ Circuit breakers
- ✅ API error handling
- ✅ Reconnection logic

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Disclaimer

⚠️ **Trading crypto is risky.** This bot is for educational purposes. Use at your own risk. Always backtest before live trading.

## License

MIT
