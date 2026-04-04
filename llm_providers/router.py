"""Model Router - Automatic provider selection and failover."""
import logging
from typing import Any, Dict, List, Optional
from llm_providers.provider import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes LLM requests to the best available provider with failover."""

    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}
        self.priority_order: List[str] = []
        self.default_provider: Optional[str] = None

    def add_provider(self, provider: LLMProvider, priority: int = 10) -> None:
        self.providers[provider.name] = provider
        self.priority_order.append(provider.name)
        self.priority_order.sort(key=lambda n: priority)
        if not self.default_provider:
            self.default_provider = provider.name

    async def chat(self, messages: List[Dict[str, str]], provider: str = None,
                   model: str = None, **kwargs) -> LLMResponse:
        """Route a chat request to the best available provider."""
        if provider and provider in self.providers:
            return await self.providers[provider].chat(messages, model=model, **kwargs)

        for name in self.priority_order:
            p = self.providers[name]
            try:
                response = await p.chat(messages, model=model, **kwargs)
                if not response.content.startswith("Error:"):
                    return response
            except Exception as e:
                logger.warning(f"Provider {name} failed: {e}")
                continue

        return LLMResponse(content="All providers failed", model="none", provider="none")

    async def health_check_all(self) -> Dict[str, bool]:
        results = {}
        for name, provider in self.providers.items():
            results[name] = await provider.health_check()
        return results

    def get_stats(self) -> Dict[str, Any]:
        return {
            "providers": {name: p.get_stats() for name, p in self.providers.items()},
            "default": self.default_provider,
            "priority": self.priority_order,
        }
