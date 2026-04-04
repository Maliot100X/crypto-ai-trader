"""Ollama Local LLM Provider."""
import time
import logging
import aiohttp
from typing import Any, Dict, List, Optional
from llm_providers.provider import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """Provider for local Ollama LLM runtime."""

    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3"):
        super().__init__(name="ollama", base_url=base_url)
        self.default_model = default_model

    async def chat(self, messages: List[Dict[str, str]], model: str = None,
                   temperature: float = 0.7, max_tokens: int = 2048) -> LLMResponse:
        model = model or self.default_model
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json={"model": model, "messages": messages, "stream": False,
                           "options": {"temperature": temperature, "num_predict": max_tokens}},
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as resp:
                    data = await resp.json()
                    self.total_calls += 1
                    content = data.get("message", {}).get("content", "")
                    tokens = data.get("eval_count", len(content.split()))
                    self.total_tokens += tokens
                    return LLMResponse(
                        content=content, model=model, provider="ollama",
                        tokens_used=tokens, latency_ms=(time.time() - start) * 1000, raw=data,
                    )
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return LLMResponse(content=f"Error: {e}", model=model, provider="ollama",
                               latency_ms=(time.time() - start) * 1000)

    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    self.healthy = resp.status == 200
                    return self.healthy
        except Exception:
            self.healthy = False
            return False

    async def list_models(self) -> List[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as resp:
                    data = await resp.json()
                    return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []
