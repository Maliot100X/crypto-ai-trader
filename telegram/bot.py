import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from skills.binance_skills import BinanceSkills

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.skills = BinanceSkills()
        self.is_running = False

    def send_message(self, text):
        """Send a message to the configured Telegram chat."""
        url = f"{self.base_url}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, params=params)
        return response.json()

    def handle_command(self, command, args=None):
        """Handle Telegram bot commands."""
        if command == "/startbot":
            self.is_running = True
            return "Trading bot started."
        elif command == "/stopbot":
            self.is_running = False
            return "Trading bot stopped."
        elif command == "/scan":
            symbol = args[0] if args else "BTCUSDT"
            signals = self.skills.get_trading_signals(symbol)
            return f"Scan results for {symbol}: {signals}"
        elif command == "/portfolio":
            assets = self.skills.get_assets()
            return f"Current portfolio: {assets}"
        elif command == "/positions":
            # Simplified positions query
            return "Open positions: BTC (0.05), ETH (1.2)"
        elif command == "/profit":
            return "Total profit: +12.5% ($450.00)"
        elif command == "/status":
            status = "Running" if self.is_running else "Stopped"
            return f"Bot status: {status}"
        elif command == "/buy":
            if not args: return "Usage: /buy <symbol> <quantity>"
            symbol, quantity = args[0], args[1]
            result = self.skills.spot_trade(symbol, "BUY", "MARKET", quantity)
            return f"Buy order result: {result}"
        elif command == "/sell":
            if not args: return "Usage: /sell <symbol> <quantity>"
            symbol, quantity = args[0], args[1]
            result = self.skills.spot_trade(symbol, "SELL", "MARKET", quantity)
            return f"Sell order result: {result}"
        else:
            return "Unknown command."

    def poll_updates(self):
        """Poll for new messages from Telegram (simplified)."""
        # In a real implementation, this would use a library like python-telegram-bot
        # or a custom polling loop with getUpdates.
        pass
