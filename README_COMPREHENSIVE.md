# 🚀 Autonomous Crypto Trading Platform

A complete, production-ready autonomous cryptocurrency trading platform powered by **Binance Skills Hub**, **AI reasoning**, and **24/7 Telegram bot control**. Built with real-time market analysis, advanced risk management, and multi-strategy trading capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)

---

## 🎯 Features

### Core Trading Capabilities
- **Multi-Exchange Support**: Binance Spot, Futures (USDS-M, Coin, Options), Margin, and P2P trading
- **18 Official Binance Skills**: Complete integration of all Binance Skills Hub modules
- **Multiple Trading Modes**: Spot, Futures (with leverage up to 5x), Margin, and Derivatives
- **Order Types**: Market, Limit, Stop Loss, Take Profit, Trailing Stop, OCO, OPO, OPOCO, OTO, OTOCO
- **Real-Time Signals**: AI-generated trading signals based on technical analysis

### AI & Intelligence
- **OpenAI Integration**: Codex-powered AI reasoning engine for market analysis
- **Multi-Strategy Engine**: 
  - Breakout Strategy
  - Momentum Strategy
  - Mean Reversion Strategy
  - Whale Tracking Strategy
- **Technical Indicators**: RSI, MACD, EMA, VWAP, Volume Analysis

### Risk Management
- **Position Sizing**: Automatic 5% max position size enforcement
- **Daily Loss Limits**: 10% maximum daily loss threshold
- **Leverage Control**: Max 5x leverage with automatic enforcement
- **Mandatory Stop Loss**: Every trade includes calculated stop loss and take profit
- **Portfolio Monitoring**: Real-time balance and exposure tracking

### Control & Monitoring
- **24/7 Telegram Bot**: Full command interface with rich UI
- **Real-Time Dashboard**: React-based portfolio visualization
- **Automation Loop**: Market scanning every 30 seconds
- **Trade History**: Complete audit trail of all trades
- **Performance Analytics**: Win rate, profit/loss tracking, and metrics

### Deployment
- **Vercel Ready**: React dashboard deployable to Vercel
- **Docker Support**: Containerized Python backend
- **GitHub Integration**: Professional repository setup with CI/CD ready

---

## 📦 Project Structure

```
crypto-ai-trader/
├── config/                          # Configuration & settings
│   └── settings.py                 # API keys, risk rules, intervals
├── skills/                         # Binance Skills Hub implementations (18 skills)
│   ├── spot/                       # Spot trading skill
│   ├── derivatives-trading-usds-futures/  # USDS-M Futures
│   ├── derivatives-trading-coin-futures/  # Coin Futures
│   ├── derivatives-trading-options/       # Options trading
│   ├── margin-trading/             # Margin trading
│   ├── alpha/                      # Alpha signals
│   ├── assets/                     # Asset management
│   ├── p2p/                        # P2P trading
│   ├── convert/                    # Crypto conversion
│   ├── fiat/                       # Fiat integration
│   ├── onchain-pay/                # On-chain payments
│   ├── simple-earn/                # Staking & earning
│   ├── sub-account/                # Sub-account management
│   ├── vip-loan/                   # VIP loan services
│   ├── algo/                       # Algorithmic trading
│   ├── square-post/                # Binance Square integration
│   └── binance_skills.py           # Unified skills interface
├── binance/                        # Core trading engine
│   └── trading_engine.py           # Binance API wrapper
├── ai/                             # AI reasoning engine
│   └── reasoning_engine.py         # OpenAI integration
├── strategies/                     # Trading strategies
│   └── strategy_engine.py          # Multi-strategy orchestration
├── signals/                        # Technical indicators
│   └── indicators.py               # RSI, MACD, EMA, VWAP, Volume
├── risk/                           # Risk management
│   └── risk_manager.py             # Position sizing & validation
├── execution/                      # Order execution
├── telegram/                       # Telegram bot
│   ├── bot.py                      # Basic bot interface
│   └── telegram_bot_24_7.py        # 24/7 bot with full commands
├── core/                           # Automation & orchestration
│   └── orchestrator.py             # Main automation loop
├── dashboard/                      # React dashboard
│   ├── client/src/pages/Dashboard.tsx  # Main dashboard UI
│   └── ...                         # React components
└── README.md                       # This file
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 16+ (for dashboard)
- Binance API credentials
- OpenAI OAuth credentials
- Telegram Bot token

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/crypto-ai-trader.git
cd crypto-ai-trader
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Credentials
Edit `config/settings.py`:
```python
BINANCE_API_KEY = "your_api_key"
BINANCE_SECRET_KEY = "your_secret_key"
OPENAI_OAUTH_CLIENT_ID = "your_client_id"
OPENAI_OAUTH_CLIENT_SECRET = "your_secret"
OPENAI_REDIRECT_URI = "your_redirect_uri"
TELEGRAM_BOT_TOKEN = "8785140526:AAGbzhIxdJSG43U1jCuKfv0zGaaPIGmWUGs"
TELEGRAM_CHAT_ID = "7764037225"
```

### Step 4: Install Dashboard Dependencies
```bash
cd dashboard
npm install
```

---

## 🚀 Usage

### Start the Trading Bot (24/7)
```bash
python telegram/telegram_bot_24_7.py
```

### Start the Automation Loop
```bash
python core/orchestrator.py
```

### Start the Dashboard (Development)
```bash
cd dashboard
npm run dev
```

### Build Dashboard for Production
```bash
npm run build
```

---

## 📱 Telegram Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/startbot` | Start the trading bot | `/startbot` |
| `/stopbot` | Stop the trading bot | `/stopbot` |
| `/scan` | Scan market for signals | `/scan` |
| `/portfolio` | View portfolio status | `/portfolio` |
| `/positions` | View open positions | `/positions` |
| `/profit` | View profit/loss | `/profit` |
| `/status` | Check bot status | `/status` |
| `/buy` | Execute buy order | `/buy BTCUSDT 0.001` |
| `/sell` | Execute sell order | `/sell BTCUSDT 0.001` |
| `/help` | Show help message | `/help` |

---

## 🤖 AI Reasoning Engine

The platform uses OpenAI's Codex model to analyze market conditions and make trading decisions:

```python
from ai.reasoning_engine import OpenAIReasoningEngine

engine = OpenAIReasoningEngine()
engine.authenticate(code)

# AI analyzes market data and calls system tools
decision = engine.reason_and_act(market_data, portfolio_status)
```

**System Tools Available to AI:**
- `scan_market(symbol)` - Analyze market conditions
- `place_order(symbol, side, type, quantity)` - Execute trades
- `close_position(symbol)` - Close open positions
- `portfolio_status()` - Get current portfolio

---

## 📊 Trading Strategies

### 1. Breakout Strategy
Identifies price breakouts above/below 20-period highs/lows.

### 2. Momentum Strategy
Uses RSI and MACD crossovers to identify momentum shifts.

### 3. Mean Reversion Strategy
Trades price reversions to EMA with RSI extremes.

### 4. Whale Tracking Strategy
Detects volume spikes indicating large trader activity.

---

## 🛡️ Risk Management

All trades are protected by:
- **Position Size Limit**: Max 5% of portfolio per trade
- **Daily Loss Limit**: Stop trading if daily loss exceeds 10%
- **Mandatory Stop Loss**: Every trade includes calculated SL
- **Take Profit Targets**: Automatic profit-taking at 5% gains
- **Leverage Limits**: Maximum 5x leverage on futures

---

## 📈 Technical Indicators

- **RSI (Relative Strength Index)**: Overbought/oversold detection
- **MACD**: Trend and momentum analysis
- **EMA (Exponential Moving Average)**: Trend identification
- **VWAP**: Volume-weighted average price
- **Volume MA**: Volume trend analysis

---

## 🌐 Binance Skills Hub Integration

The platform integrates all 18 official Binance Skills:

1. **Spot Trading** - Buy/sell on spot market
2. **USDS-M Futures** - USD-margined perpetual futures
3. **Coin Futures** - Coin-margined perpetual futures
4. **Options** - Options trading
5. **Margin Trading** - Leveraged spot trading
6. **Alpha** - Market insights and signals
7. **Assets** - Portfolio and balance management
8. **P2P Trading** - Peer-to-peer trading
9. **Crypto Conversion** - Instant crypto swaps
10. **Fiat Integration** - Fiat on/off ramps
11. **On-Chain Pay** - Direct wallet transfers
12. **Simple Earn** - Staking and yield products
13. **Sub-Accounts** - Multi-account management
14. **VIP Loans** - Collateralized lending
15. **Algorithmic Trading** - Advanced order types
16. **Square Posts** - Social platform integration
17. **Portfolio Margin** - Advanced margin trading
18. **Portfolio Margin Pro** - Professional margin trading

---

## 🔐 Security

- **API Key Encryption**: Credentials stored securely
- **Rate Limiting**: Respects Binance API limits
- **Order Validation**: All orders validated before execution
- **Audit Trail**: Complete trade history logging
- **Error Handling**: Comprehensive error recovery

---

## 📊 Dashboard Features

The React dashboard provides:
- Real-time portfolio value tracking
- Open positions monitoring
- Trading signals visualization
- Performance analytics
- Bot status and control
- Trade history

---

## 🚀 Deployment

### Deploy Dashboard to Vercel
```bash
cd dashboard
npm run build
vercel deploy
```

### Deploy Bot to Cloud Server
```bash
# Using Docker
docker build -t crypto-trader .
docker run -d crypto-trader

# Or using systemd
sudo systemctl start crypto-trader
```

---

## 📝 Configuration

### Risk Rules
```python
RISK_RULES = {
    "max_position_size": 0.05,  # 5%
    "max_daily_loss": 0.10,     # 10%
    "max_leverage": 5,          # 5x
    "stop_loss_required": True
}
```

### Automation Settings
```python
SCAN_INTERVAL = 30  # seconds
```

---

## 🐛 Troubleshooting

### Bot Not Responding
- Check Telegram bot token
- Verify internet connection
- Check logs: `tail -f logs/bot.log`

### API Errors
- Verify Binance API credentials
- Check API key permissions
- Ensure sufficient account balance

### Dashboard Not Loading
- Clear browser cache
- Check Node.js version
- Verify npm dependencies: `npm install`

---

## 📚 API Documentation

### Binance Trading Engine
```python
from binance.trading_engine import BinanceTradingEngine

engine = BinanceTradingEngine(api_key, secret_key)

# Spot trading
engine.place_spot_order("BTCUSDT", "BUY", "MARKET", 0.001)

# Futures trading
engine.place_futures_order("BTCUSDT", "BUY", "MARKET", 1, leverage=5)

# Margin trading
engine.place_margin_order("BTCUSDT", "BUY", "MARKET", 0.001)
```

### Strategy Engine
```python
from strategies.strategy_engine import StrategyEngine

strategy = StrategyEngine()
signal = strategy.generate_combined_signal(df)  # Returns "BUY", "SELL", or "HOLD"
```

### Risk Manager
```python
from risk.risk_manager import RiskManager

rm = RiskManager()
is_valid, msg = rm.validate_trade(portfolio_balance, trade_amount, daily_loss_pct)
sl_price = rm.calculate_stop_loss(entry_price, "BUY")
tp_price = rm.calculate_take_profit(entry_price, "BUY")
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For support, email support@cryptotrader.com or open an issue on GitHub.

---

## ⚠️ Disclaimer

This software is provided for educational and research purposes only. Cryptocurrency trading carries risk. Always conduct your own research and consult with financial advisors before trading. The authors are not responsible for any losses incurred.

---

## 🎉 Acknowledgments

- Binance for the official Skills Hub
- OpenAI for the Codex reasoning engine
- The open-source community for excellent libraries

---

**Made with ❤️ by the Crypto AI Trader Team**
