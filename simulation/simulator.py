"""Trading Simulator - Full simulation of multi-agent trading."""
import asyncio
import logging
import random
from typing import Any, Dict, List
from datetime import datetime
from agents.runtime import AgentRuntime
from trading_engine.market_data import MarketDataService
from trading_engine.signals import SignalGenerator
from trading_engine.strategy_manager import StrategyManager
from trading_engine.executor import TradeExecutor
from trading_engine.position_manager import PositionManager
from trading_engine.risk_manager import RiskManager

logger = logging.getLogger(__name__)


class TradingSimulator:
    """Runs a complete trading simulation with multiple agents."""

    def __init__(self, num_agents: int = 3, initial_capital: float = 10000.0):
        self.num_agents = num_agents
        self.initial_capital = initial_capital
        self.runtime = AgentRuntime()
        self.market_data = MarketDataService()
        self.signal_gen = SignalGenerator()
        self.strategy_mgr = StrategyManager()
        self.executor = TradeExecutor(mode="simulation")
        self.position_mgr = PositionManager()
        self.risk_mgr = RiskManager()
        self.risk_mgr.current_equity = initial_capital
        self.risk_mgr.peak_equity = initial_capital
        self.simulation_log: List[Dict[str, Any]] = []

    def setup_agents(self) -> None:
        """Create and configure agents for simulation."""
        personalities = ["aggressive", "conservative", "analytical", "momentum", "contrarian"]
        for i in range(self.num_agents):
            config = {
                "personality": personalities[i % len(personalities)],
                "cycle_interval": 5,
            }
            self.runtime.create_agent(f"agent_{i+1}", config)
        logger.info(f"Created {self.num_agents} simulation agents")

    async def run_simulation(self, cycles: int = 50, symbol: str = "SOL/USD") -> Dict[str, Any]:
        """Run a complete trading simulation."""
        self.setup_agents()
        results = {
            "symbol": symbol,
            "cycles": cycles,
            "agents": self.num_agents,
            "initial_capital": self.initial_capital,
            "trades": [],
            "signals": [],
        }

        prices_history = []

        for cycle in range(cycles):
            price_data = await self.market_data.get_price(symbol)
            current_price = price_data["price"]
            prices_history.append(current_price)

            # Generate signals
            if len(prices_history) >= 26:
                signals = self.signal_gen.generate_signals(prices_history, symbol)
                strategy_signals = self.strategy_mgr.evaluate_all(prices_history)
                all_signals = signals + strategy_signals
                results["signals"].extend(all_signals)

                # Process signals through risk manager
                for sig in all_signals:
                    action = sig.get("action", "hold")
                    if action in ("buy", "sell"):
                        size = self.initial_capital * 0.1 / current_price
                        risk_check = self.risk_mgr.check_trade(
                            action, size, current_price, self.risk_mgr.current_equity)
                        if risk_check["approved"]:
                            order = await self.executor.execute(
                                symbol, action, risk_check["adjusted_size"], current_price,
                                stop_loss=risk_check.get("stop_loss", 0),
                                take_profit=risk_check.get("take_profit", 0),
                            )
                            results["trades"].append(vars(order))
                            if action == "buy":
                                self.position_mgr.open_position(
                                    symbol, action, risk_check["adjusted_size"], current_price,
                                    risk_check.get("stop_loss", 0), risk_check.get("take_profit", 0))
                                self.risk_mgr.open_positions += 1
                            elif action == "sell" and symbol in self.position_mgr.positions:
                                closed = self.position_mgr.close_position(symbol, current_price)
                                if closed:
                                    self.risk_mgr.update_pnl(
                                        closed.get("realized_pnl", 0), self.risk_mgr.current_equity)
                                    self.risk_mgr.open_positions -= 1

            # Update positions
            if symbol in self.position_mgr.positions:
                self.position_mgr.update_price(symbol, current_price)
                stop_hit = self.position_mgr.check_stops(symbol, current_price)
                if stop_hit:
                    closed = self.position_mgr.close_position(symbol, current_price)
                    logger.info(f"[SIM] {stop_hit} triggered at {current_price}")

            self.simulation_log.append({
                "cycle": cycle, "price": current_price,
                "positions": len(self.position_mgr.positions),
                "equity": round(self.risk_mgr.current_equity + self.position_mgr.get_portfolio_value(), 2),
            })

        # Final stats
        pos_stats = self.position_mgr.get_stats()
        risk_status = self.risk_mgr.get_risk_status()
        results["final_equity"] = round(self.risk_mgr.current_equity + self.position_mgr.get_portfolio_value(), 2)
        results["total_trades"] = len(results["trades"])
        results["position_stats"] = pos_stats
        results["risk_status"] = risk_status
        results["roi_pct"] = round(((results["final_equity"] - self.initial_capital) / self.initial_capital) * 100, 2)
        results["simulation_log"] = self.simulation_log

        return results
