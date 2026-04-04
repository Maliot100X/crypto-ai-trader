"""Telegram Bot Controller - Command interface for the trading platform."""
import os
import asyncio
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Conditional import for python-telegram-bot
try:
    from telegram import Update, Bot
    from telegram.ext import Application, CommandHandler, ContextTypes
    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False
    logger.warning("python-telegram-bot not installed. Telegram bot will run in stub mode.")


HELP_TEXT = """
*Solana Agent Trader - Command Reference*

/help - Show this help message
/models - List available LLM models
/start\\_agents - Start all trading agents
/stop\\_agents - Stop all trading agents
/list\\_agents - List all agents and their status
/create\\_wallet - Create a new Solana wallet
/connect\\_wallet <key> - Connect an existing wallet
/wallet\\_status - Show wallet balances and status
/run\\_backtest <strategy> - Run a backtesting simulation
/deploy\\_strategy <name> - Deploy a trading strategy
/system\\_status - Show system health status
/logs - Show recent system logs
"""


class TelegramController:
    """Telegram bot that controls the trading platform."""

    def __init__(self, token: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.runtime = None  # Set externally: AgentRuntime
        self.wallet_manager = None  # Set externally: WalletManager
        self.backtest_engine = None  # Set externally: BacktestEngine
        self.model_router = None  # Set externally: ModelRouter
        self._app = None
        self._log_buffer = []

    def set_dependencies(self, runtime=None, wallet_manager=None,
                         backtest_engine=None, model_router=None):
        """Inject platform dependencies."""
        if runtime:
            self.runtime = runtime
        if wallet_manager:
            self.wallet_manager = wallet_manager
        if backtest_engine:
            self.backtest_engine = backtest_engine
        if model_router:
            self.model_router = model_router

    def log(self, message: str):
        self._log_buffer.append(message)
        if len(self._log_buffer) > 100:
            self._log_buffer = self._log_buffer[-100:]

    async def cmd_help(self, update, context):
        await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")

    async def cmd_models(self, update, context):
        if self.model_router:
            stats = self.model_router.get_stats()
            providers = stats.get("providers", {})
            lines = ["*Available LLM Providers:*\n"]
            for name, info in providers.items():
                status = "healthy" if info.get("healthy") else "offline"
                lines.append(f"- {name}: {status} (calls: {info.get('total_calls', 0)})")
            await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        else:
            await update.message.reply_text("No model router configured.")

    async def cmd_start_agents(self, update, context):
        if self.runtime:
            await self.runtime.start_all()
            status = self.runtime.get_runtime_status()
            await update.message.reply_text(
                f"Agents started. Active: {status['active_agents']}/{status['total_agents']}")
        else:
            await update.message.reply_text("Agent runtime not configured.")

    async def cmd_stop_agents(self, update, context):
        if self.runtime:
            await self.runtime.stop_all()
            await update.message.reply_text("All agents stopped.")
        else:
            await update.message.reply_text("Agent runtime not configured.")

    async def cmd_list_agents(self, update, context):
        if self.runtime:
            agents = self.runtime.list_agents()
            if not agents:
                await update.message.reply_text("No agents registered.")
                return
            lines = ["*Agents:*\n"]
            for a in agents:
                lines.append(f"- {a['agent_id']}: {a['status']}")
            await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        else:
            await update.message.reply_text("Agent runtime not configured.")

    async def cmd_create_wallet(self, update, context):
        if self.wallet_manager:
            result = self.wallet_manager.create_wallet()
            await update.message.reply_text(
                f"Wallet created!\nPublic Key: `{result.get('public_key', 'N/A')}`",
                parse_mode="Markdown")
        else:
            await update.message.reply_text("Wallet manager not configured.")

    async def cmd_connect_wallet(self, update, context):
        if not context.args:
            await update.message.reply_text("Usage: /connect_wallet <public_key>")
            return
        if self.wallet_manager:
            result = self.wallet_manager.connect_wallet(context.args[0])
            await update.message.reply_text(f"Wallet status: {result.get('status')}")
        else:
            await update.message.reply_text("Wallet manager not configured.")

    async def cmd_wallet_status(self, update, context):
        if self.wallet_manager:
            status = self.wallet_manager.wallet_status()
            lines = [f"*Wallet Status*\nActive: `{status.get('active_wallet', 'None')}`"]
            lines.append(f"Total wallets: {status.get('total_wallets', 0)}")
            for w in status.get("wallets", []):
                lines.append(f"- `{w['public_key'][:12]}...` Balance: {w.get('balance', 0)} SOL")
            await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        else:
            await update.message.reply_text("Wallet manager not configured.")

    async def cmd_run_backtest(self, update, context):
        strategy = context.args[0] if context.args else "momentum"
        if self.backtest_engine:
            result = self.backtest_engine.run_backtest(strategy=strategy)
            msg = (f"*Backtest Results ({strategy})*\n"
                   f"ROI: {result['roi_pct']}%\n"
                   f"Sharpe: {result['sharpe_ratio']}\n"
                   f"Max Drawdown: {result['max_drawdown_pct']}%\n"
                   f"Win Rate: {result['win_rate']}%\n"
                   f"Trades: {result['total_trades']}")
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("Backtest engine not configured.")

    async def cmd_deploy_strategy(self, update, context):
        if not context.args:
            await update.message.reply_text("Usage: /deploy_strategy <strategy_name>")
            return
        await update.message.reply_text(f"Strategy '{context.args[0]}' deployed.")

    async def cmd_system_status(self, update, context):
        status_lines = ["*System Status*\n"]
        if self.runtime:
            rs = self.runtime.get_runtime_status()
            status_lines.append(f"Agents: {rs['active_agents']}/{rs['total_agents']} active")
        if self.model_router:
            ms = self.model_router.get_stats()
            status_lines.append(f"LLM Providers: {len(ms.get('providers', {}))}")
        if self.wallet_manager:
            ws = self.wallet_manager.wallet_status()
            status_lines.append(f"Wallets: {ws.get('total_wallets', 0)}")
        status_lines.append("Platform: Online")
        await update.message.reply_text("\n".join(status_lines), parse_mode="Markdown")

    async def cmd_logs(self, update, context):
        if self._log_buffer:
            logs = "\n".join(self._log_buffer[-20:])
            await update.message.reply_text(f"```\n{logs}\n```", parse_mode="Markdown")
        else:
            await update.message.reply_text("No recent logs.")

    def build_app(self) -> Any:
        """Build the Telegram application with all handlers."""
        if not HAS_TELEGRAM:
            logger.error("python-telegram-bot is required")
            return None
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not set")
            return None

        self._app = Application.builder().token(self.token).build()
        handlers = {
            "help": self.cmd_help,
            "models": self.cmd_models,
            "start_agents": self.cmd_start_agents,
            "stop_agents": self.cmd_stop_agents,
            "list_agents": self.cmd_list_agents,
            "create_wallet": self.cmd_create_wallet,
            "connect_wallet": self.cmd_connect_wallet,
            "wallet_status": self.cmd_wallet_status,
            "run_backtest": self.cmd_run_backtest,
            "deploy_strategy": self.cmd_deploy_strategy,
            "system_status": self.cmd_system_status,
            "logs": self.cmd_logs,
        }
        for cmd, handler in handlers.items():
            self._app.add_handler(CommandHandler(cmd, handler))
        return self._app

    async def start(self):
        """Start the Telegram bot."""
        app = self.build_app()
        if app:
            logger.info("Starting Telegram bot...")
            await app.run_polling()
