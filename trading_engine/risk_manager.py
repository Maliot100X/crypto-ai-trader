"""Risk Manager - Position sizing and risk controls."""
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RiskLimits:
    max_position_pct: float = 0.1  # Max 10% of portfolio per position
    max_daily_loss_pct: float = 0.05  # Max 5% daily loss
    max_drawdown_pct: float = 0.15  # Max 15% drawdown
    max_open_positions: int = 10
    stop_loss_pct: float = 0.03  # 3% stop loss
    take_profit_pct: float = 0.06  # 6% take profit


class RiskManager:
    """Manages risk controls for trading operations."""

    def __init__(self, limits: RiskLimits = None):
        self.limits = limits or RiskLimits()
        self.daily_pnl = 0.0
        self.peak_equity = 0.0
        self.current_equity = 0.0
        self.open_positions = 0

    def check_trade(self, action: str, size: float, price: float,
                    portfolio_value: float) -> Dict[str, Any]:
        """Validate a trade against risk limits."""
        position_value = size * price
        position_pct = position_value / portfolio_value if portfolio_value > 0 else 1.0

        if position_pct > self.limits.max_position_pct:
            return {"approved": False, "reason": f"Position size {position_pct:.1%} exceeds limit {self.limits.max_position_pct:.1%}"}

        if self.open_positions >= self.limits.max_open_positions:
            return {"approved": False, "reason": f"Max open positions ({self.limits.max_open_positions}) reached"}

        daily_loss_pct = abs(self.daily_pnl / portfolio_value) if portfolio_value > 0 else 0
        if self.daily_pnl < 0 and daily_loss_pct >= self.limits.max_daily_loss_pct:
            return {"approved": False, "reason": "Daily loss limit reached"}

        drawdown = (self.peak_equity - self.current_equity) / self.peak_equity if self.peak_equity > 0 else 0
        if drawdown >= self.limits.max_drawdown_pct:
            return {"approved": False, "reason": f"Max drawdown {drawdown:.1%} reached"}

        adjusted_size = min(size, (portfolio_value * self.limits.max_position_pct) / price) if price > 0 else size

        return {
            "approved": True,
            "original_size": size,
            "adjusted_size": round(adjusted_size, 6),
            "stop_loss": round(price * (1 - self.limits.stop_loss_pct), 4) if action == "buy" else round(price * (1 + self.limits.stop_loss_pct), 4),
            "take_profit": round(price * (1 + self.limits.take_profit_pct), 4) if action == "buy" else round(price * (1 - self.limits.take_profit_pct), 4),
        }

    def update_pnl(self, pnl: float, equity: float) -> None:
        self.daily_pnl += pnl
        self.current_equity = equity
        if equity > self.peak_equity:
            self.peak_equity = equity

    def reset_daily(self) -> None:
        self.daily_pnl = 0.0

    def get_risk_status(self) -> Dict[str, Any]:
        drawdown = (self.peak_equity - self.current_equity) / self.peak_equity if self.peak_equity > 0 else 0
        return {
            "daily_pnl": round(self.daily_pnl, 4),
            "drawdown_pct": round(drawdown * 100, 2),
            "open_positions": self.open_positions,
            "peak_equity": round(self.peak_equity, 2),
            "current_equity": round(self.current_equity, 2),
            "limits": {
                "max_position_pct": self.limits.max_position_pct,
                "max_daily_loss_pct": self.limits.max_daily_loss_pct,
                "max_drawdown_pct": self.limits.max_drawdown_pct,
            },
        }
