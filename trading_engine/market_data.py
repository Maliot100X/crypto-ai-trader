"""Market Data Service - Real-time and historical market data."""
import asyncio
import logging
import random
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class OHLCV:
    """OHLCV candlestick data."""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class OrderBook:
    """Order book snapshot."""
    symbol: str
    bids: List[List[float]] = field(default_factory=list)
    asks: List[List[float]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MarketDataService:
    """Provides real-time and historical market data for trading agents."""

    def __init__(self, data_sources: List[str] = None):
        self.data_sources = data_sources or ["simulation"]
        self._price_cache: Dict[str, float] = {}
        self._history_cache: Dict[str, List[OHLCV]] = {}
        self._subscribers: Dict[str, List] = {}

    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol."""
        if "simulation" in self.data_sources:
            price = self._simulate_price(symbol)
        else:
            price = self._price_cache.get(symbol, 0.0)
        self._price_cache[symbol] = price
        return {
            "symbol": symbol,
            "price": price,
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.data_sources[0],
        }

    async def get_ohlcv(self, symbol: str, timeframe: str = "1h",
                        limit: int = 100) -> List[Dict[str, Any]]:
        """Get historical OHLCV data."""
        candles = []
        base_price = self._price_cache.get(symbol, 100.0)
        now = datetime.utcnow()
        for i in range(limit):
            t = now - timedelta(hours=limit - i)
            o = base_price * (1 + random.uniform(-0.02, 0.02))
            h = o * (1 + random.uniform(0, 0.03))
            l = o * (1 - random.uniform(0, 0.03))
            c = random.uniform(l, h)
            v = random.uniform(1000, 100000)
            candles.append({"timestamp": t.isoformat(), "open": round(o, 4), "high": round(h, 4),
                            "low": round(l, 4), "close": round(c, 4), "volume": round(v, 2)})
            base_price = c
        return candles

    async def get_orderbook(self, symbol: str, depth: int = 20) -> Dict[str, Any]:
        """Get order book snapshot."""
        mid_price = self._price_cache.get(symbol, 100.0)
        bids = [[round(mid_price * (1 - i * 0.001), 4), round(random.uniform(1, 100), 2)]
                for i in range(1, depth + 1)]
        asks = [[round(mid_price * (1 + i * 0.001), 4), round(random.uniform(1, 100), 2)]
                for i in range(1, depth + 1)]
        return {"symbol": symbol, "bids": bids, "asks": asks,
                "timestamp": datetime.utcnow().isoformat()}

    async def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get 24h ticker data."""
        price = self._price_cache.get(symbol, 100.0)
        change = random.uniform(-5, 5)
        return {
            "symbol": symbol, "price": round(price, 4),
            "change_24h": round(change, 2),
            "volume_24h": round(random.uniform(100000, 10000000), 2),
            "high_24h": round(price * 1.05, 4),
            "low_24h": round(price * 0.95, 4),
        }

    def _simulate_price(self, symbol: str) -> float:
        """Generate a simulated price with random walk."""
        base_prices = {"SOL/USD": 150.0, "BTC/USD": 65000.0, "ETH/USD": 3500.0}
        current = self._price_cache.get(symbol, base_prices.get(symbol, 100.0))
        change = current * random.uniform(-0.005, 0.005)
        return round(current + change, 4)

    async def subscribe(self, symbol: str, callback) -> None:
        """Subscribe to price updates."""
        self._subscribers.setdefault(symbol, []).append(callback)

    async def start_feed(self, symbols: List[str], interval: float = 1.0) -> None:
        """Start simulated price feed."""
        while True:
            for symbol in symbols:
                price_data = await self.get_price(symbol)
                for cb in self._subscribers.get(symbol, []):
                    await cb(price_data)
            await asyncio.sleep(interval)
