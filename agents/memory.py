"""Agent Memory Store - Persistent and working memory for agents."""
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """A single memory entry."""
    key: str
    value: Any
    category: str  # "market", "trade", "strategy", "observation"
    importance: float = 0.5  # 0.0 to 1.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ttl: Optional[int] = None  # seconds until expiry, None = permanent


class MemoryStore:
    """
    Memory system for autonomous agents.

    Supports:
    - Short-term working memory (recent observations)
    - Long-term memory (learned patterns, trade history)
    - Episodic memory (specific trading events)
    """

    def __init__(self, agent_id: str, max_short_term: int = 100, max_long_term: int = 10000):
        self.agent_id = agent_id
        self.short_term: deque = deque(maxlen=max_short_term)
        self.long_term: Dict[str, MemoryEntry] = {}
        self.episodes: List[Dict[str, Any]] = []
        self.trade_history: List[Dict[str, Any]] = []
        self._max_long_term = max_long_term

    def remember(self, key: str, value: Any, category: str = "observation",
                 importance: float = 0.5, ttl: Optional[int] = None) -> None:
        """Store a memory entry."""
        entry = MemoryEntry(
            key=key, value=value, category=category,
            importance=importance, ttl=ttl,
        )
        self.short_term.append(entry)
        if importance >= 0.7:
            self.long_term[key] = entry
            if len(self.long_term) > self._max_long_term:
                self._evict_least_important()

    def recall(self, key: str) -> Optional[Any]:
        """Recall a specific memory by key."""
        if key in self.long_term:
            return self.long_term[key].value
        for entry in reversed(self.short_term):
            if entry.key == key:
                return entry.value
        return None

    def recall_recent(self, category: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        """Recall recent memories, optionally filtered by category."""
        entries = list(self.short_term)
        if category:
            entries = [e for e in entries if e.category == category]
        return entries[-limit:]

    def record_trade(self, trade: Dict[str, Any]) -> None:
        """Record a trade in episodic memory."""
        trade["timestamp"] = datetime.utcnow().isoformat()
        self.trade_history.append(trade)
        self.remember(
            key=f"trade_{len(self.trade_history)}",
            value=trade,
            category="trade",
            importance=0.8,
        )

    def record_episode(self, episode: Dict[str, Any]) -> None:
        """Record a significant event."""
        episode["timestamp"] = datetime.utcnow().isoformat()
        self.episodes.append(episode)

    def get_context_window(self, max_entries: int = 20) -> List[Dict[str, Any]]:
        """Get recent context for LLM reasoning."""
        recent = self.recall_recent(limit=max_entries)
        return [{"key": e.key, "value": e.value, "category": e.category} for e in recent]

    def get_trade_stats(self) -> Dict[str, Any]:
        """Get summary statistics of trade history."""
        if not self.trade_history:
            return {"total_trades": 0}
        wins = [t for t in self.trade_history if t.get("pnl", 0) > 0]
        losses = [t for t in self.trade_history if t.get("pnl", 0) < 0]
        total_pnl = sum(t.get("pnl", 0) for t in self.trade_history)
        return {
            "total_trades": len(self.trade_history),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": len(wins) / len(self.trade_history) if self.trade_history else 0,
            "total_pnl": round(total_pnl, 4),
        }

    def _evict_least_important(self) -> None:
        """Remove least important long-term memories when at capacity."""
        if not self.long_term:
            return
        sorted_keys = sorted(self.long_term.keys(), key=lambda k: self.long_term[k].importance)
        for key in sorted_keys[:len(self.long_term) // 10]:
            del self.long_term[key]

    def export_state(self) -> Dict[str, Any]:
        """Export memory state for persistence."""
        return {
            "agent_id": self.agent_id,
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "episodes_count": len(self.episodes),
            "trade_stats": self.get_trade_stats(),
        }
