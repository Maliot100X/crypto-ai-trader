"""Agent Runtime - Async multi-agent execution environment."""
import asyncio
import logging
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from agents.brain import AgentBrain
from agents.memory import MemoryStore
from agents.skill_loader import SkillLoader
from agents.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class Agent:
    """Autonomous trading agent with brain, memory, skills, and tools."""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.brain = AgentBrain(agent_id, personality=self.config.get("personality", "analytical"))
        self.memory = MemoryStore(agent_id)
        self.skill_loader = SkillLoader()
        self.tool_registry = ToolRegistry()
        self.status = "idle"
        self.created_at = datetime.utcnow().isoformat()
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start agent execution loop."""
        self.status = "running"
        logger.info(f"Agent {self.agent_id} started")
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        """Stop agent execution."""
        self.status = "stopped"
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Agent {self.agent_id} stopped")

    async def _run_loop(self) -> None:
        """Main agent execution loop."""
        cycle = 0
        while self.status == "running":
            try:
                cycle += 1
                context = await self._gather_context()
                chain = await self.brain.reason(context)
                if chain.conclusion:
                    decision = json.loads(chain.conclusion)
                    self.memory.remember(
                        key=f"decision_{cycle}",
                        value=decision,
                        category="strategy",
                        importance=decision.get("confidence", 0.5),
                    )
                    if decision.get("confidence", 0) > 0.7:
                        await self._execute_decision(decision)
                await asyncio.sleep(self.config.get("cycle_interval", 30))
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Agent {self.agent_id} loop error: {e}")
                self.memory.record_episode({"type": "error", "error": str(e)})
                await asyncio.sleep(5)

    async def _gather_context(self) -> Dict[str, Any]:
        """Gather current market context for reasoning."""
        return {
            "agent_id": self.agent_id,
            "cycle_time": datetime.utcnow().isoformat(),
            "memory_context": self.memory.get_context_window(10),
            "trade_stats": self.memory.get_trade_stats(),
            "available_tools": len(self.tool_registry.list_tools()),
            "price_change_pct": 0.0,
            "volume_spike": False,
            "sentiment_score": 0.5,
        }

    async def _execute_decision(self, decision: Dict[str, Any]) -> None:
        """Execute a trading decision."""
        action = decision.get("action", "hold")
        if action in ("buy", "sell", "accumulate"):
            self.memory.record_trade({
                "action": action,
                "confidence": decision.get("confidence", 0),
                "reasoning": decision.get("reasoning", ""),
                "simulated": True,
            })
            logger.info(f"Agent {self.agent_id} executed: {action} (confidence: {decision.get('confidence')})")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "created_at": self.created_at,
            "memory": self.memory.export_state(),
            "tools": self.tool_registry.get_stats(),
            "skills": self.skill_loader.export_registry(),
        }


class AgentRuntime:
    """Multi-agent runtime manager."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self._running = False

    def create_agent(self, agent_id: str, config: Dict[str, Any] = None) -> Agent:
        """Create and register a new agent."""
        agent = Agent(agent_id, config)
        self.agents[agent_id] = agent
        logger.info(f"Created agent: {agent_id}")
        return agent

    async def start_all(self) -> None:
        """Start all agents."""
        self._running = True
        for agent in self.agents.values():
            await agent.start()
        logger.info(f"Started {len(self.agents)} agents")

    async def stop_all(self) -> None:
        """Stop all agents."""
        self._running = False
        for agent in self.agents.values():
            await agent.stop()
        logger.info("All agents stopped")

    async def start_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            await self.agents[agent_id].start()
            return True
        return False

    async def stop_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            await self.agents[agent_id].stop()
            return True
        return False

    def list_agents(self) -> List[Dict[str, Any]]:
        return [agent.get_status() for agent in self.agents.values()]

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def get_runtime_status(self) -> Dict[str, Any]:
        return {
            "running": self._running,
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.status == "running"),
            "agents": {aid: a.status for aid, a in self.agents.items()},
        }
