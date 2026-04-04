"""Base LLM Provider abstraction."""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    provider: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    raw: Optional[Dict[str, Any]] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, name: str, base_url: str = "", api_key: str = ""):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.healthy = False
        self.total_calls = 0
        self.total_tokens = 0

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], model: str = None,
                   temperature: float = 0.7, max_tokens: int = 2048) -> LLMResponse:
        """Send a chat completion request."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is healthy."""
        pass

    def get_stats(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "healthy": self.healthy,
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
        }
