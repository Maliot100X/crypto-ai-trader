"""Tool Registry - Central registry for all agent tools."""
import logging
import asyncio
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ToolDefinition:
    """Definition for a registered tool."""
    name: str
    description: str
    handler: Optional[Callable] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    category: str = "general"
    enabled: bool = True
    call_count: int = 0
    last_called: Optional[str] = None


class ToolRegistry:
    """Central registry for all tools available to agents."""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._categories: Dict[str, List[str]] = {}

    def register(self, name: str, description: str, handler: Callable,
                 parameters: Dict[str, Any] = None, category: str = "general") -> None:
        """Register a tool."""
        tool = ToolDefinition(
            name=name, description=description, handler=handler,
            parameters=parameters or {}, category=category,
        )
        self._tools[name] = tool
        self._categories.setdefault(category, []).append(name)
        logger.info(f"Registered tool: {name} [{category}]")

    async def invoke(self, name: str, **kwargs) -> Any:
        """Invoke a registered tool."""
        if name not in self._tools:
            raise ValueError(f"Tool not found: {name}")
        tool = self._tools[name]
        if not tool.enabled:
            raise RuntimeError(f"Tool disabled: {name}")
        tool.call_count += 1
        tool.last_called = datetime.utcnow().isoformat()
        handler = tool.handler
        if asyncio.iscoroutinefunction(handler):
            return await handler(**kwargs)
        return handler(**kwargs)

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        tools = self._tools.values()
        if category:
            tools = [t for t in tools if t.category == category]
        return [{"name": t.name, "description": t.description, "category": t.category} for t in tools]

    def get_categories(self) -> List[str]:
        return list(self._categories.keys())

    def disable_tool(self, name: str) -> None:
        if name in self._tools:
            self._tools[name].enabled = False

    def enable_tool(self, name: str) -> None:
        if name in self._tools:
            self._tools[name].enabled = True

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_tools": len(self._tools),
            "categories": len(self._categories),
            "total_calls": sum(t.call_count for t in self._tools.values()),
            "tools_by_category": {cat: len(tools) for cat, tools in self._categories.items()},
        }

    def export_for_llm(self) -> List[Dict[str, Any]]:
        """Export tool definitions in LLM-friendly format."""
        return [
            {"name": t.name, "description": t.description, "parameters": t.parameters}
            for t in self._tools.values() if t.enabled
        ]
