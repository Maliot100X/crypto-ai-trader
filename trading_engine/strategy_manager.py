"""Strategy Manager - Trading strategy orchestration."""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Strategy:
    """Trading strategy definition."""
    name: str
    type: str  # momentum, mean_reversion, ai_signal, sentiment, arbitrage
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    performance: Dict[str, float] = field(default_factory=lambda: {"total_pnl": 0.0, "trades": 0, "win_rate": 0.0})


class StrategyManager:
    """Manages and orchestrates multiple trading strategies."""

    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self._register_default_strategies()

    def _register_default_strategies(self):
        defaults = [
            Strategy("momentum_breakout", "momentum", {"lookback": 20, "threshold": 2.0}),
            Strategy("mean_reversion", "mean_reversion", {"period": 20, "std_dev": 2.0}),
            Strategy("ai_signal", "ai_signal", {"confidence_threshold": 0.7}),
            Strategy("sentiment_trade", "sentiment", {"positive_threshold": 0.7, "negative_threshold": 0.3}),
            Strategy("cross_exchange_arb", "arbitrage", {"min_spread": 0.5}),
        ]
        for s in defaults:
            self.strategies[s.name] = s

    def evaluate_momentum(self, prices: List[float], params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        lookback = params.get("lookback", 20)
        threshold = params.get("threshold", 2.0)
        if len(prices) < lookback:
            return None
        recent = prices[-lookback:]
        pct_change = ((recent[-1] - recent[0]) / recent[0]) * 100
        if abs(pct_change) >= threshold:
            return {"strategy": "momentum", "action": "buy" if pct_change > 0 else "sell",
                    "strength": round(abs(pct_change) / threshold, 2),
                    "pct_change": round(pct_change, 2)}
        return None

    def evaluate_mean_reversion(self, prices: List[float], params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        period = params.get("period", 20)
        std_mult = params.get("std_dev", 2.0)
        if len(prices) < period:
            return None
        import math
        window = prices[-period:]
        mean = sum(window) / period
        std = math.sqrt(sum((p - mean) ** 2 for p in window) / period)
        current = prices[-1]
        z_score = (current - mean) / std if std > 0 else 0
        if z_score < -std_mult:
            return {"strategy": "mean_reversion", "action": "buy", "z_score": round(z_score, 2)}
        elif z_score > std_mult:
            return {"strategy": "mean_reversion", "action": "sell", "z_score": round(z_score, 2)}
        return None

    def evaluate_all(self, prices: List[float], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Evaluate all enabled strategies against current data."""
        signals = []
        for name, strategy in self.strategies.items():
            if not strategy.enabled:
                continue
            result = None
            if strategy.type == "momentum":
                result = self.evaluate_momentum(prices, strategy.parameters)
            elif strategy.type == "mean_reversion":
                result = self.evaluate_mean_reversion(prices, strategy.parameters)
            elif strategy.type == "ai_signal" and context:
                ai_confidence = context.get("ai_confidence", 0)
                if ai_confidence > strategy.parameters.get("confidence_threshold", 0.7):
                    result = {"strategy": "ai_signal", "action": context.get("ai_action", "hold"),
                              "confidence": ai_confidence}
            if result:
                result["timestamp"] = datetime.utcnow().isoformat()
                signals.append(result)
        return signals

    def deploy_strategy(self, name: str) -> bool:
        if name in self.strategies:
            self.strategies[name].enabled = True
            return True
        return False

    def disable_strategy(self, name: str) -> bool:
        if name in self.strategies:
            self.strategies[name].enabled = False
            return True
        return False

    def list_strategies(self) -> List[Dict[str, Any]]:
        return [{"name": s.name, "type": s.type, "enabled": s.enabled,
                 "performance": s.performance} for s in self.strategies.values()]
