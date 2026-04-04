"""Comprehensive test suite for Solana Agent Trader platform."""
import sys
import os
import asyncio
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAgentBrain(unittest.TestCase):
    """Test the AgentBrain reasoning engine."""

    def test_brain_creation(self):
        from agents.brain import AgentBrain
        brain = AgentBrain("test_agent", personality="analytical")
        self.assertEqual(brain.agent_id, "test_agent")
        self.assertEqual(brain.personality, "analytical")

    def test_brain_reasoning(self):
        from agents.brain import AgentBrain
        brain = AgentBrain("test_agent")
        context = {"price_change_pct": 3.0, "volume_spike": True, "sentiment_score": 0.7}
        chain = asyncio.get_event_loop().run_until_complete(brain.reason(context))
        self.assertIsNotNone(chain.conclusion)
        self.assertTrue(len(chain.steps) > 0)

    def test_brain_plan_strategy(self):
        from agents.brain import AgentBrain
        brain = AgentBrain("test_agent")
        market_state = {"price_change_pct": 5.0, "volume_spike": True, "sentiment_score": 0.8}
        actions = asyncio.get_event_loop().run_until_complete(brain.plan_strategy(market_state))
        self.assertIsInstance(actions, list)


class TestMemoryStore(unittest.TestCase):
    """Test the MemoryStore."""

    def test_memory_creation(self):
        from agents.memory import MemoryStore
        mem = MemoryStore("test_agent")
        self.assertEqual(mem.agent_id, "test_agent")

    def test_remember_recall(self):
        from agents.memory import MemoryStore
        mem = MemoryStore("test_agent")
        mem.remember("price_sol", 150.0, category="market", importance=0.8)
        self.assertEqual(mem.recall("price_sol"), 150.0)

    def test_trade_recording(self):
        from agents.memory import MemoryStore
        mem = MemoryStore("test_agent")
        mem.record_trade({"action": "buy", "price": 150.0, "pnl": 10.0})
        stats = mem.get_trade_stats()
        self.assertEqual(stats["total_trades"], 1)

    def test_context_window(self):
        from agents.memory import MemoryStore
        mem = MemoryStore("test_agent")
        for i in range(5):
            mem.remember(f"key_{i}", f"value_{i}")
        ctx = mem.get_context_window(3)
        self.assertEqual(len(ctx), 3)


class TestToolRegistry(unittest.TestCase):
    """Test the ToolRegistry."""

    def test_register_and_invoke(self):
        from agents.tool_registry import ToolRegistry
        registry = ToolRegistry()
        registry.register("test_tool", "A test tool", lambda x=1: x * 2, category="test")
        tools = registry.list_tools()
        self.assertEqual(len(tools), 1)
        result = asyncio.get_event_loop().run_until_complete(registry.invoke("test_tool", x=5))
        self.assertEqual(result, 10)

    def test_tool_stats(self):
        from agents.tool_registry import ToolRegistry
        registry = ToolRegistry()
        registry.register("t1", "Tool 1", lambda: 1, category="a")
        registry.register("t2", "Tool 2", lambda: 2, category="b")
        stats = registry.get_stats()
        self.assertEqual(stats["total_tools"], 2)
        self.assertEqual(stats["categories"], 2)


class TestSkillLoader(unittest.TestCase):
    """Test the SkillLoader."""

    def test_skill_loader_creation(self):
        from agents.skill_loader import SkillLoader
        loader = SkillLoader("skills")
        self.assertEqual(len(loader.loaded_skills), 0)

    def test_scan_skills_directory(self):
        from agents.skill_loader import SkillLoader
        loader = SkillLoader("skills")
        count = loader.load_all()
        self.assertGreaterEqual(count, 0)

    def test_export_registry(self):
        from agents.skill_loader import SkillLoader
        loader = SkillLoader("skills")
        registry = loader.export_registry()
        self.assertIn("total_skills", registry)


class TestAgentRuntime(unittest.TestCase):
    """Test the AgentRuntime."""

    def test_create_agent(self):
        from agents.runtime import AgentRuntime
        runtime = AgentRuntime()
        agent = runtime.create_agent("test_1", {"personality": "aggressive"})
        self.assertEqual(agent.agent_id, "test_1")
        self.assertEqual(len(runtime.agents), 1)

    def test_list_agents(self):
        from agents.runtime import AgentRuntime
        runtime = AgentRuntime()
        runtime.create_agent("a1")
        runtime.create_agent("a2")
        agents = runtime.list_agents()
        self.assertEqual(len(agents), 2)

    def test_runtime_status(self):
        from agents.runtime import AgentRuntime
        runtime = AgentRuntime()
        runtime.create_agent("a1")
        status = runtime.get_runtime_status()
        self.assertEqual(status["total_agents"], 1)
        self.assertFalse(status["running"])


class TestTradingEngine(unittest.TestCase):
    """Test the Trading Engine components."""

    def test_market_data(self):
        from trading_engine.market_data import MarketDataService
        mds = MarketDataService()
        price = asyncio.get_event_loop().run_until_complete(mds.get_price("SOL/USD"))
        self.assertIn("price", price)
        self.assertGreater(price["price"], 0)

    def test_signal_generator(self):
        from trading_engine.signals import SignalGenerator
        gen = SignalGenerator()
        prices = [100 + i * 0.5 for i in range(30)]
        rsi = gen.compute_rsi(prices)
        self.assertGreater(rsi, 0)
        self.assertLessEqual(rsi, 100)

    def test_macd(self):
        from trading_engine.signals import SignalGenerator
        gen = SignalGenerator()
        prices = [100 + i * 0.3 for i in range(30)]
        macd = gen.compute_macd(prices)
        self.assertIn("macd", macd)
        self.assertIn("signal", macd)

    def test_strategy_manager(self):
        from trading_engine.strategy_manager import StrategyManager
        mgr = StrategyManager()
        strategies = mgr.list_strategies()
        self.assertGreater(len(strategies), 0)

    def test_risk_manager(self):
        from trading_engine.risk_manager import RiskManager
        rm = RiskManager()
        result = rm.check_trade("buy", 1.0, 150.0, 10000.0)
        self.assertTrue(result["approved"])

    def test_risk_position_limit(self):
        from trading_engine.risk_manager import RiskManager
        rm = RiskManager()
        # Try to buy more than 10% of portfolio
        result = rm.check_trade("buy", 100.0, 150.0, 10000.0)
        self.assertFalse(result["approved"])

    def test_trade_executor(self):
        from trading_engine.executor import TradeExecutor
        executor = TradeExecutor(mode="simulation")
        order = asyncio.get_event_loop().run_until_complete(
            executor.execute("SOL/USD", "buy", 1.0, 150.0))
        self.assertEqual(order.status, "filled")
        self.assertEqual(order.side, "buy")

    def test_position_manager(self):
        from trading_engine.position_manager import PositionManager
        pm = PositionManager()
        pm.open_position("SOL/USD", "buy", 1.0, 150.0, stop_loss=145.0, take_profit=160.0)
        self.assertEqual(len(pm.positions), 1)
        pm.update_price("SOL/USD", 155.0)
        self.assertGreater(pm.positions["SOL/USD"]["unrealized_pnl"], 0)
        closed = pm.close_position("SOL/USD", 155.0)
        self.assertEqual(closed["realized_pnl"], 5.0)


class TestBacktesting(unittest.TestCase):
    """Test the Backtesting Engine."""

    def test_backtest_run(self):
        from backtesting.engine import BacktestEngine
        engine = BacktestEngine(initial_capital=10000.0)
        result = engine.run_backtest(strategy="momentum", days=100)
        self.assertIn("roi_pct", result)
        self.assertIn("sharpe_ratio", result)
        self.assertIn("max_drawdown_pct", result)
        self.assertIn("total_trades", result)

    def test_backtest_mean_reversion(self):
        from backtesting.engine import BacktestEngine
        engine = BacktestEngine()
        result = engine.run_backtest(strategy="mean_reversion", days=100)
        self.assertIn("final_equity", result)


class TestWalletManager(unittest.TestCase):
    """Test wallet operations."""

    def test_create_wallet(self):
        from solana.client import SolanaClient
        client = SolanaClient()
        result = client.create_wallet()
        self.assertEqual(result["status"], "created")
        self.assertIn("public_key", result)

    def test_list_wallets(self):
        from solana.client import SolanaClient
        client = SolanaClient()
        client.create_wallet()
        client.create_wallet()
        wallets = client.list_wallets()
        self.assertEqual(len(wallets), 2)

    def test_wallet_manager(self):
        from wallet_manager.manager import WalletManager
        wm = WalletManager()
        result = wm.create_wallet()
        self.assertEqual(result["status"], "created")
        status = wm.wallet_status()
        self.assertEqual(status["total_wallets"], 1)


class TestSkillRegistry(unittest.TestCase):
    """Test skill discovery."""

    def test_crawler(self):
        from skills.registry.crawler import RepositoryCrawler
        crawler = RepositoryCrawler()
        repos = crawler.get_repository_manifest()
        self.assertGreater(len(repos), 0)

    def test_local_skill_scan(self):
        from skills.registry.crawler import RepositoryCrawler
        crawler = RepositoryCrawler()
        skills = crawler.crawl_local_skills("skills")
        self.assertIsInstance(skills, list)


class TestTelegramBot(unittest.TestCase):
    """Test Telegram bot controller."""

    def test_controller_creation(self):
        from telegram_bot.controller import TelegramController
        bot = TelegramController(token="test_token")
        self.assertEqual(bot.token, "test_token")

    def test_help_text(self):
        from telegram_bot.controller import HELP_TEXT
        self.assertIn("/help", HELP_TEXT)
        self.assertIn("create", HELP_TEXT)
        self.assertIn("wallet", HELP_TEXT)
        self.assertIn("system", HELP_TEXT)


if __name__ == "__main__":
    unittest.main()
