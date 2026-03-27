import os

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "8785140526:AAGbzhIxdJSG43U1jCuKfv0zGaaPIGmWUGs"
TELEGRAM_CHAT_ID = "7764037225"

# Binance Configuration (Placeholders)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")

# OpenAI OAuth Configuration (Placeholders)
OPENAI_OAUTH_CLIENT_ID = os.getenv("OPENAI_OAUTH_CLIENT_ID", "")
OPENAI_OAUTH_CLIENT_SECRET = os.getenv("OPENAI_OAUTH_CLIENT_SECRET", "")
OPENAI_REDIRECT_URI = os.getenv("OPENAI_REDIRECT_URI", "")

# Risk Management Rules
RISK_RULES = {
    "max_position_size": 0.05,  # 5 percent
    "max_daily_loss": 0.10,     # 10 percent
    "max_leverage": 5,          # 5x
    "stop_loss_required": True
}

# Automation Settings
SCAN_INTERVAL = 30  # seconds
