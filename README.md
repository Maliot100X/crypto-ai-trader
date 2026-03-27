# Autonomous Crypto Trading Platform

A complete autonomous crypto trading platform integrating Binance Skills Hub, Binance Trading APIs, OpenAI AI reasoning, and Telegram bot control interface.

## Features

- **Binance Skills Hub Integration**: Native access to Binance Spot, Futures, Margin, Alpha, and Assets skills.
- **AI Reasoning Engine**: Powered by OpenAI Codex for market analysis and decision-making.
- **Trading Engine**: Support for spot, futures, and margin trading with market, limit, stop loss, and take profit orders.
- **Strategy Engine**: Implements breakout, momentum, mean reversion, and whale tracking strategies.
- **Risk Management**: Automated position sizing, daily loss limits, and mandatory stop loss rules.
- **Telegram Bot Interface**: Full control and monitoring via Telegram commands.
- **Automation Loop**: Scans market, updates indicators, generates signals, evaluates risk, and executes trades every 30 seconds.

## Project Structure

- `config/`: Configuration and risk management rules.
- `skills/`: Implementation of Binance Skills Hub modules.
- `binance/`: Core trading engine for Binance APIs.
- `ai/`: OpenAI OAuth and reasoning engine.
- `strategies/`: Trading strategies and signal generation.
- `signals/`: Technical indicators (RSI, MACD, EMA, VWAP, Volume).
- `risk/`: Risk management and trade validation.
- `execution/`: Order execution logic.
- `telegram/`: Telegram bot control interface.
- `core/`: Automation loop and orchestration core.

## Setup

1. Provide the required credentials in `config/settings.py`.
2. Install dependencies: `pip install requests pandas numpy`.
3. Run the orchestrator: `python core/orchestrator.py`.

## Telegram Commands

- `/startbot`: Start the trading bot.
- `/stopbot`: Stop the trading bot.
- `/scan`: Scan market for signals.
- `/portfolio`: View current portfolio.
- `/positions`: View open positions.
- `/profit`: View total profit.
- `/status`: Check bot status.
- `/buy`: Execute a buy order.
- `/sell`: Execute a sell order.

