"""Backtesting Engine - Run strategies against historical data."""
import math
import random
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BacktestEngine:
    """Backtests trading strategies with performance metrics."""

    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.results: Dict[str, Any] = {}

    def generate_price_series(self, start_price: float = 100.0, days: int = 365,
                               volatility: float = 0.02) -> List[Dict[str, Any]]:
        """Generate simulated price series for backtesting."""
        prices = []
        price = start_price
        now = datetime.utcnow()
        for i in range(days):
            t = now - timedelta(days=days - i)
            change = random.gauss(0, volatility)
            price *= (1 + change)
            prices.append({
                "timestamp": t.isoformat(), "open": round(price * 0.999, 4),
                "high": round(price * (1 + abs(random.gauss(0, 0.01))), 4),
                "low": round(price * (1 - abs(random.gauss(0, 0.01))), 4),
                "close": round(price, 4), "volume": round(random.uniform(10000, 500000), 2),
            })
        return prices

    def run_backtest(self, strategy: str = "momentum", symbol: str = "SOL/USD",
                     days: int = 365, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run a complete backtest."""
        params = params or {}
        prices = self.generate_price_series(
            start_price=params.get("start_price", 150.0),
            days=days,
            volatility=params.get("volatility", 0.025),
        )

        capital = self.initial_capital
        position = 0.0
        entry_price = 0.0
        trades = []
        equity_curve = [capital]
        close_prices = [p["close"] for p in prices]

        for i in range(20, len(close_prices)):
            window = close_prices[i-20:i]
            current = close_prices[i]

            signal = self._evaluate_strategy(strategy, window, current, params)

            if signal == "buy" and position == 0:
                size = (capital * 0.95) / current
                position = size
                entry_price = current
                capital -= size * current
                trades.append({"type": "buy", "price": current, "size": size,
                               "day": i, "timestamp": prices[i]["timestamp"]})

            elif signal == "sell" and position > 0:
                pnl = (current - entry_price) * position
                capital += position * current
                trades.append({"type": "sell", "price": current, "size": position,
                               "pnl": round(pnl, 4), "day": i, "timestamp": prices[i]["timestamp"]})
                position = 0
                entry_price = 0

            equity = capital + position * current
            equity_curve.append(equity)

        # Close any open position
        if position > 0:
            final_price = close_prices[-1]
            pnl = (final_price - entry_price) * position
            capital += position * final_price
            trades.append({"type": "sell", "price": final_price, "size": position,
                           "pnl": round(pnl, 4), "day": len(close_prices) - 1})

        final_equity = capital
        self.results = self._compute_metrics(equity_curve, trades, final_equity)
        self.results["strategy"] = strategy
        self.results["symbol"] = symbol
        self.results["days"] = days
        self.results["total_trades"] = len(trades)
        self.results["trades"] = trades[:50]  # Keep first 50 for logging
        return self.results

    def _evaluate_strategy(self, strategy: str, window: List[float],
                           current: float, params: Dict[str, Any]) -> str:
        if strategy == "momentum":
            pct_change = (current - window[0]) / window[0] * 100
            threshold = params.get("threshold", 3.0)
            if pct_change > threshold:
                return "buy"
            elif pct_change < -threshold:
                return "sell"

        elif strategy == "mean_reversion":
            mean = sum(window) / len(window)
            std = math.sqrt(sum((p - mean) ** 2 for p in window) / len(window))
            z = (current - mean) / std if std > 0 else 0
            if z < -1.5:
                return "buy"
            elif z > 1.5:
                return "sell"

        elif strategy == "ai_signal":
            # Simulated AI signal
            if random.random() > 0.7:
                return "buy" if random.random() > 0.5 else "sell"

        return "hold"

    def _compute_metrics(self, equity_curve: List[float], trades: List[Dict],
                          final_equity: float) -> Dict[str, Any]:
        roi = ((final_equity - self.initial_capital) / self.initial_capital) * 100
        sell_trades = [t for t in trades if t["type"] == "sell" and "pnl" in t]
        wins = [t for t in sell_trades if t["pnl"] > 0]

        # Sharpe ratio (simplified)
        if len(equity_curve) > 1:
            returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
                       for i in range(1, len(equity_curve)) if equity_curve[i-1] > 0]
            mean_ret = sum(returns) / len(returns) if returns else 0
            std_ret = math.sqrt(sum((r - mean_ret) ** 2 for r in returns) / len(returns)) if returns else 1
            sharpe = (mean_ret / std_ret) * math.sqrt(252) if std_ret > 0 else 0
        else:
            sharpe = 0

        # Max drawdown
        peak = equity_curve[0]
        max_dd = 0
        for eq in equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)

        return {
            "initial_capital": self.initial_capital,
            "final_equity": round(final_equity, 2),
            "roi_pct": round(roi, 2),
            "sharpe_ratio": round(sharpe, 3),
            "max_drawdown_pct": round(max_dd * 100, 2),
            "win_rate": round(len(wins) / len(sell_trades) * 100, 1) if sell_trades else 0,
            "total_sell_trades": len(sell_trades),
        }
