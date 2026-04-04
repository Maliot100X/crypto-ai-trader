"""Signal Generator - Technical analysis and trading signals."""
import math
import logging
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class SignalGenerator:
    """Generates trading signals from market data using technical indicators."""

    def __init__(self):
        self.active_signals: List[Dict[str, Any]] = []

    def compute_sma(self, prices: List[float], period: int) -> List[float]:
        """Simple Moving Average."""
        if len(prices) < period:
            return []
        return [sum(prices[i:i+period]) / period for i in range(len(prices) - period + 1)]

    def compute_ema(self, prices: List[float], period: int) -> List[float]:
        """Exponential Moving Average."""
        if not prices:
            return []
        multiplier = 2 / (period + 1)
        ema = [prices[0]]
        for price in prices[1:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        return ema

    def compute_rsi(self, prices: List[float], period: int = 14) -> float:
        """Relative Strength Index."""
        if len(prices) < period + 1:
            return 50.0
        deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        gains = [d if d > 0 else 0 for d in deltas[-period:]]
        losses = [-d if d < 0 else 0 for d in deltas[-period:]]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    def compute_macd(self, prices: List[float]) -> Dict[str, float]:
        """MACD indicator."""
        ema12 = self.compute_ema(prices, 12)
        ema26 = self.compute_ema(prices, 26)
        if not ema12 or not ema26:
            return {"macd": 0, "signal": 0, "histogram": 0}
        macd_line = ema12[-1] - ema26[-1]
        signal_line = self.compute_ema([e12 - e26 for e12, e26 in zip(ema12[-9:], ema26[-9:])], 9)
        sig = signal_line[-1] if signal_line else 0
        return {"macd": round(macd_line, 4), "signal": round(sig, 4),
                "histogram": round(macd_line - sig, 4)}

    def compute_bollinger_bands(self, prices: List[float], period: int = 20,
                                 std_dev: float = 2.0) -> Dict[str, float]:
        """Bollinger Bands."""
        if len(prices) < period:
            return {"upper": 0, "middle": 0, "lower": 0}
        window = prices[-period:]
        middle = sum(window) / period
        variance = sum((p - middle) ** 2 for p in window) / period
        std = math.sqrt(variance)
        return {"upper": round(middle + std_dev * std, 4),
                "middle": round(middle, 4),
                "lower": round(middle - std_dev * std, 4)}

    def generate_signals(self, prices: List[float], symbol: str = "SOL/USD") -> List[Dict[str, Any]]:
        """Generate trading signals from price data."""
        signals = []
        if len(prices) < 26:
            return signals

        rsi = self.compute_rsi(prices)
        macd = self.compute_macd(prices)
        bb = self.compute_bollinger_bands(prices)
        current_price = prices[-1]

        # RSI signals
        if rsi < 30:
            signals.append({"type": "rsi_oversold", "symbol": symbol, "strength": "strong",
                            "action": "buy", "rsi": rsi})
        elif rsi > 70:
            signals.append({"type": "rsi_overbought", "symbol": symbol, "strength": "strong",
                            "action": "sell", "rsi": rsi})

        # MACD crossover
        if macd["histogram"] > 0 and macd["macd"] > macd["signal"]:
            signals.append({"type": "macd_bullish", "symbol": symbol, "strength": "medium",
                            "action": "buy", "macd": macd})
        elif macd["histogram"] < 0:
            signals.append({"type": "macd_bearish", "symbol": symbol, "strength": "medium",
                            "action": "sell", "macd": macd})

        # Bollinger Band signals
        if current_price <= bb["lower"]:
            signals.append({"type": "bb_lower_touch", "symbol": symbol, "strength": "medium",
                            "action": "buy", "bb": bb})
        elif current_price >= bb["upper"]:
            signals.append({"type": "bb_upper_touch", "symbol": symbol, "strength": "medium",
                            "action": "sell", "bb": bb})

        for sig in signals:
            sig["timestamp"] = datetime.utcnow().isoformat()

        self.active_signals.extend(signals)
        return signals
