# 🚀 Setup Guide - Autonomous Crypto Trading Platform

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/Maliot100X/crypto-ai-trader.git
cd crypto-ai-trader
```

### 2. Configure Credentials
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
cd dashboard && npm install && cd ..
```

### 4. Start Services

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Manual Start**
```bash
# Terminal 1: Start Telegram Bot
python telegram/telegram_bot_24_7.py

# Terminal 2: Start Dashboard
cd dashboard && npm run dev

# Terminal 3: Start Automation Loop
python core/orchestrator.py
```

## Detailed Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (optional)
- Binance Account with API keys
- OpenAI OAuth credentials
- Telegram Bot token

### Step-by-Step Installation

#### 1. Get Binance API Keys
1. Go to https://www.binance.com/en/account/api-management
2. Create new API key
3. Enable "Spot & Margin Trading Commission"
4. Copy API Key and Secret Key

#### 2. Get OpenAI OAuth Credentials
1. Visit https://platform.openai.com/account/api-keys
2. Create OAuth application
3. Note Client ID, Client Secret, and Redirect URI

#### 3. Create Telegram Bot
1. Message @BotFather on Telegram
2. Create new bot and get token
3. Get your Telegram Chat ID from @userinfobot

#### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env`:
```
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret
OPENAI_OAUTH_CLIENT_ID=your_client_id
OPENAI_OAUTH_CLIENT_SECRET=your_secret
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

#### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 6. Install Dashboard Dependencies
```bash
cd dashboard
npm install
cd ..
```

### Running the Platform

#### Start Telegram Bot (24/7)
```bash
python telegram/telegram_bot_24_7.py
```

#### Start Dashboard (Development)
```bash
cd dashboard
npm run dev
# Access at http://localhost:3000
```

#### Start Automation Loop
```bash
python core/orchestrator.py
```

#### Using Docker
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Deployment

### Deploy Dashboard to Vercel
```bash
cd dashboard
npm run build
vercel deploy
```

### Deploy Bot to Cloud Server

**Using Railway:**
```bash
railway login
railway init
railway up
```

**Using Render:**
1. Connect GitHub repository
2. Create new Web Service
3. Set environment variables
4. Deploy

**Using AWS Lambda:**
```bash
# Package bot for Lambda
zip -r lambda-function.zip .
# Upload to AWS Lambda
```

## Testing

### Test Telegram Bot
```bash
# Send command to bot
/startbot
/scan
/portfolio
```

### Test Trading Engine
```bash
python -c "from binance.trading_engine import BinanceTradingEngine; engine = BinanceTradingEngine(); print(engine.get_portfolio_status())"
```

### Test Dashboard
```bash
cd dashboard
npm run dev
# Open http://localhost:3000
```

## Troubleshooting

### Bot Not Responding
- Check token in `.env`
- Verify internet connection
- Check logs: `tail -f logs/bot.log`

### API Errors
- Verify credentials
- Check API key permissions
- Ensure account balance

### Dashboard Not Loading
- Clear cache: `Ctrl+Shift+Delete`
- Check Node version: `node --version`
- Reinstall deps: `npm install`

## Security Best Practices

1. **Never commit credentials**
   - Use `.env` files (in `.gitignore`)
   - Use environment variables in production

2. **API Key Permissions**
   - Enable only required permissions
   - Use IP whitelist
   - Rotate keys regularly

3. **Telegram Bot**
   - Use strong bot token
   - Restrict chat ID access
   - Monitor bot activity

4. **Database**
   - Use encrypted connections
   - Regular backups
   - Audit logs

## Performance Optimization

### Reduce API Calls
- Increase `SCAN_INTERVAL` (default: 30s)
- Cache market data
- Batch API requests

### Improve Dashboard
- Enable caching
- Optimize images
- Use CDN

### Scale Bot
- Use message queues
- Horizontal scaling
- Load balancing

## Monitoring

### Check Bot Status
```bash
# View running processes
ps aux | grep python

# Check logs
tail -f logs/bot.log

# Monitor resources
top
```

### Monitor Dashboard
```bash
# Check Node process
ps aux | grep node

# View build size
npm run build -- --analyze
```

## Support

- Documentation: See README.md
- Issues: GitHub Issues
- Email: support@cryptotrader.com

## Next Steps

1. ✅ Configure credentials
2. ✅ Install dependencies
3. ✅ Start services
4. ✅ Test bot commands
5. ✅ Monitor performance
6. ✅ Deploy to production

Happy trading! 🚀
