"""Trade Executor - Executes trades across exchanges and DEXs."""
import logging
from typing import Any, Dict, List
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TradeOrder:
    order_id: str
    symbol: str
    side: str  # buy/sell
    size: float
    price: float
    order_type: str = "market"  # market/limit
    status: str = "pending"
    stop_loss: float = 0.0
    take_profit: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    fill_price: float = 0.0
    filled_at: str = ""


class TradeExecutor:
    """Executes trading orders (simulation and live)."""

    def __init__(self, mode: str = "simulation"):
        self.mode = mode
        self.order_history: List[TradeOrder] = []
        self._order_counter = 0

    async def execute(self, symbol: str, side: str, size: float, price: float,
                      order_type: str = "market", stop_loss: float = 0, take_profit: float = 0) -> TradeOrder:
        self._order_counter += 1
        order = TradeOrder(
            order_id=f"ORD-{self._order_counter:06d}",
            symbol=symbol, side=side, size=size, price=price,
            order_type=order_type, stop_loss=stop_loss, take_profit=take_profit,
        )
        if self.mode == "simulation":
            order.status = "filled"
            order.fill_price = price
            order.filled_at = datetime.utcnow().isoformat()
            logger.info(f"[SIM] {side.upper()} {size} {symbol} @ {price}")
        else:
            order.status = "submitted"
            logger.info(f"[LIVE] Submitted {side.upper()} {size} {symbol} @ {price}")

        self.order_history.append(order)
        return order

    def get_order(self, order_id: str) -> Dict[str, Any]:
        for order in self.order_history:
            if order.order_id == order_id:
                return vars(order)
        return {}

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [vars(o) for o in self.order_history[-limit:]]
