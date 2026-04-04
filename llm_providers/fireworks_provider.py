"""Fireworks AI Provider - OpenAI-compatible endpoint."""
import os
import time
import logging
import aiohttp
from typing import Any, Dict, List
from llm_providers.provider import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class FireworksProvider(LLMProvider):
    """Provider for Fireworks AI (OpenAI-compatible)."""

    def __init__(self, api_key: str = None,
                 base_url: str = "https://api.fireworks.ai/inference/v1",
                 default_model: str = "accounts/fireworks/routers/kimi-k2p5-turbo"):
        super().__init__(name="fireworks", base_url=base_url,
                         api_key=api_key or os.getenv("FIREWORKS_API_KEY", ""))
        self.default_model = default_model

    async def chat(self, messages: List[Dict[str, str]], model: str = None,
                   temperature: float = 0.7, max_tokens: int = 2048) -> LLMResponse:
        model = model or self.default_model
        start = time.time()
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    data = await resp.json()
                    self.total_calls += 1
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    tokens = data.get("usage", {}).get("total_tokens", 0)
                    self.total_tokens += tokens
                    return LLMResponse(content=content, model=model, provider="fireworks",
                                       tokens_used=tokens, latency_ms=(time.time() - start) * 1000, raw=data)
        except Exception as e:
            logger.error(f"Fireworks chat error: {e}")
            return LLMResponse(content=f"Error: {e}", model=model, provider="fireworks",
                               latency_ms=(time.time() - start) * 1000)

    async def health_check(self) -> bool:
        if not self.api_key:
            self.healthy = False
            return False
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/models", headers=headers,
                                       timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    self.healthy = resp.status == 200
                    return self.healthy
        except Exception:
            self.healthy = False
            return False
