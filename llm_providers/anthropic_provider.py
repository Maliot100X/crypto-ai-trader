"""Anthropic API Provider."""
import os
import time
import logging
import aiohttp
from typing import Any, Dict, List
from llm_providers.provider import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Provider for Anthropic Claude API."""

    def __init__(self, api_key: str = None, base_url: str = "https://api.anthropic.com/v1",
                 default_model: str = "claude-sonnet-4-20250514"):
        super().__init__(name="anthropic", base_url=base_url, api_key=api_key or os.getenv("ANTHROPIC_API_KEY", ""))
        self.default_model = default_model

    async def chat(self, messages: List[Dict[str, str]], model: str = None,
                   temperature: float = 0.7, max_tokens: int = 2048) -> LLMResponse:
        model = model or self.default_model
        start = time.time()
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        system_msg = ""
        chat_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                chat_messages.append(m)
        try:
            body = {"model": model, "messages": chat_messages, "max_tokens": max_tokens, "temperature": temperature}
            if system_msg:
                body["system"] = system_msg
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/messages", headers=headers, json=body,
                                        timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    data = await resp.json()
                    self.total_calls += 1
                    content = ""
                    for block in data.get("content", []):
                        if block.get("type") == "text":
                            content += block.get("text", "")
                    tokens = data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)
                    self.total_tokens += tokens
                    return LLMResponse(content=content, model=model, provider="anthropic",
                                       tokens_used=tokens, latency_ms=(time.time() - start) * 1000, raw=data)
        except Exception as e:
            logger.error(f"Anthropic chat error: {e}")
            return LLMResponse(content=f"Error: {e}", model=model, provider="anthropic",
                               latency_ms=(time.time() - start) * 1000)

    async def health_check(self) -> bool:
        self.healthy = bool(self.api_key)
        return self.healthy
