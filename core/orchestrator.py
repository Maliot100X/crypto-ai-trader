import time
import pandas as pd
from config.settings import SCAN_INTERVAL
from strategies.strategy_engine import StrategyEngine
from risk.risk_manager import RiskManager
from ai.reasoning_engine import OpenAIReasoningEngine
from telegram.bot import TelegramBot
from skills.binance_skills import BinanceSkills

class TradingOrchestrator:
    def __init__(self):
        self.strategy_engine = StrategyEngine()
        self.risk_manager = RiskManager()
        self.ai_engine = OpenAIReasoningEngine()
        self.telegram_bot = TelegramBot()
        self.skills = BinanceSkills()
        self.is_running = False

    def start(self):
        """Start the automation loop."""
        self.is_running = True
        self.telegram_bot.send_message("🚀 *Autonomous Trading Platform Started*")
        self.run_loop()

    def stop(self):
        """Stop the automation loop."""
        self.is_running = False
        self.telegram_bot.send_message("🛑 *Autonomous Trading Platform Stopped*")

    def run_loop(self):
        """Main automation loop running every 30 seconds."""
        while self.is_running:
            try:
                # 1. Scan Market
                symbol = "BTCUSDT"
                # Mocking market data for demonstration
                market_data = {
                    "symbol": symbol,
                    "close": [65000, 65100, 65200, 65150, 65300],
                    "high": [65100, 65200, 65300, 65250, 65400],
                    "low": [64900, 65000, 65100, 65050, 65200],
                    "volume": [100, 120, 150, 110, 200]
                }
                df = pd.DataFrame(market_data)

                # 2. Update Indicators & Generate Signals
                signal = self.strategy_engine.generate_combined_signal(df)
                
                # 3. AI Reasoning Engine Analysis
                portfolio = self.skills.get_assets()
                ai_decision = self.ai_engine.reason_and_act(market_data, portfolio)

                # 4. Evaluate Risk & Execute Trades
                if signal == "BUY":
                    # Simplified risk check
                    portfolio_balance = 10000  # Mock balance
                    trade_amount = 500         # Mock trade amount
                    daily_loss_pct = 0.02      # Mock daily loss
                    
                    is_valid, msg = self.risk_manager.validate_trade(portfolio_balance, trade_amount, daily_loss_pct)
                    
                    if is_valid:
                        stop_loss = self.risk_manager.calculate_stop_loss(65300, "BUY")
                        take_profit = self.risk_manager.calculate_take_profit(65300, "BUY")
                        
                        # Execute trade
                        result = self.skills.spot_trade(symbol, "BUY", "MARKET", 0.001)
                        self.telegram_bot.send_message(f"✅ *Trade Executed*: BUY {symbol}\nSignal: {signal}\nSL: {stop_loss}\nTP: {take_profit}")
                    else:
                        self.telegram_bot.send_message(f"⚠️ *Risk Warning*: {msg}")

                # 5. Update Portfolio & Status
                # (Handled by AI engine and Telegram commands)

                time.sleep(SCAN_INTERVAL)
            except Exception as e:
                self.telegram_bot.send_message(f"❌ *Error in Automation Loop*: {str(e)}")
                time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    orchestrator = TradingOrchestrator()
    orchestrator.start()
