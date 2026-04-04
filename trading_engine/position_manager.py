"""Position Manager - Track and manage open positions."""
import logging
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PositionManager:
    """Tracks open positions and calculates P&L."""

    def __init__(self):
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.closed_positions: List[Dict[str, Any]] = []

    def open_position(self, symbol: str, side: str, size: float, entry_price: float,
                      stop_loss: float = 0, take_profit: float = 0) -> Dict[str, Any]:
        position = {
            "symbol": symbol, "side": side, "size": size,
            "entry_price": entry_price, "current_price": entry_price,
            "stop_loss": stop_loss, "take_profit": take_profit,
            "unrealized_pnl": 0.0, "opened_at": datetime.utcnow().isoformat(),
        }
        self.positions[symbol] = position
        return position

    def update_price(self, symbol: str, current_price: float) -> Dict[str, Any]:
        if symbol not in self.positions:
            return {}
        pos = self.positions[symbol]
        pos["current_price"] = current_price
        if pos["side"] == "buy":
            pos["unrealized_pnl"] = round((current_price - pos["entry_price"]) * pos["size"], 4)
        else:
            pos["unrealized_pnl"] = round((pos["entry_price"] - current_price) * pos["size"], 4)
        return pos

    def close_position(self, symbol: str, exit_price: float) -> Dict[str, Any]:
        if symbol not in self.positions:
            return {}
        pos = self.positions.pop(symbol)
        if pos["side"] == "buy":
            pnl = (exit_price - pos["entry_price"]) * pos["size"]
        else:
            pnl = (pos["entry_price"] - exit_price) * pos["size"]
        pos["exit_price"] = exit_price
        pos["realized_pnl"] = round(pnl, 4)
        pos["closed_at"] = datetime.utcnow().isoformat()
        self.closed_positions.append(pos)
        return pos

    def check_stops(self, symbol: str, current_price: float) -> str:
        """Check if stop loss or take profit is hit. Returns 'stop_loss', 'take_profit', or ''."""
        if symbol not in self.positions:
            return ""
        pos = self.positions[symbol]
        if pos["side"] == "buy":
            if pos["stop_loss"] > 0 and current_price <= pos["stop_loss"]:
                return "stop_loss"
            if pos["take_profit"] > 0 and current_price >= pos["take_profit"]:
                return "take_profit"
        else:
            if pos["stop_loss"] > 0 and current_price >= pos["stop_loss"]:
                return "stop_loss"
            if pos["take_profit"] > 0 and current_price <= pos["take_profit"]:
                return "take_profit"
        return ""

    def get_portfolio_value(self) -> float:
        return sum(p.get("unrealized_pnl", 0) for p in self.positions.values())

    def list_positions(self) -> List[Dict[str, Any]]:
        return list(self.positions.values())

    def get_stats(self) -> Dict[str, Any]:
        total_pnl = sum(p.get("realized_pnl", 0) for p in self.closed_positions)
        wins = [p for p in self.closed_positions if p.get("realized_pnl", 0) > 0]
        return {
            "open_positions": len(self.positions),
            "closed_positions": len(self.closed_positions),
            "total_realized_pnl": round(total_pnl, 4),
            "win_rate": round(len(wins) / len(self.closed_positions), 2) if self.closed_positions else 0,
            "unrealized_pnl": round(self.get_portfolio_value(), 4),
        }
