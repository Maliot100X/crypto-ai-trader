"""Agent Brain - LLM-powered reasoning engine for autonomous agents."""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ThoughtStep:
    """A single step in the agent's reasoning chain."""
    step_id: int
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ReasoningChain:
    """Complete chain of thought for a task."""
    task: str
    steps: List[ThoughtStep] = field(default_factory=list)
    conclusion: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None


class AgentBrain:
    """
    Core reasoning engine for an autonomous trading agent.

    Uses LLM providers to reason about market conditions,
    select strategies, and decide on tool invocations.
    """

    def __init__(self, agent_id: str, llm_provider=None, personality: str = "analytical"):
        self.agent_id = agent_id
        self.llm_provider = llm_provider
        self.personality = personality
        self.reasoning_history: List[ReasoningChain] = []
        self.system_prompt = self._build_system_prompt()
        self._running = False

    def _build_system_prompt(self) -> str:
        return f"""You are an autonomous AI trading agent (ID: {self.agent_id}).
Your personality is: {self.personality}.

You analyze market data, execute trading strategies, and manage risk.
You have access to tools for:
- Market data retrieval (prices, volume, order books)
- Technical analysis (indicators, patterns)
- Strategy execution (momentum, mean reversion, sentiment)
- Blockchain interaction (Solana wallet, DEX trading)
- Risk management (position sizing, stop losses)

When reasoning about trades:
1. Analyze current market conditions
2. Evaluate signals from multiple strategies
3. Assess risk/reward ratio
4. Make a clear decision with rationale
5. Execute or wait based on confidence level

Always output structured JSON for tool calls."""

    async def reason(self, context: Dict[str, Any]) -> ReasoningChain:
        """Execute a reasoning chain given market context."""
        chain = ReasoningChain(task=json.dumps(context))

        step1 = ThoughtStep(
            step_id=1,
            thought=f"Analyzing market context: {list(context.keys())}",
        )
        chain.steps.append(step1)

        if self.llm_provider:
            try:
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this market context and decide on action:\n{json.dumps(context, indent=2)}"},
                ]
                response = await self.llm_provider.chat(messages)
                step2 = ThoughtStep(
                    step_id=2,
                    thought="LLM analysis complete",
                    observation=response.get("content", "No response"),
                )
                chain.steps.append(step2)
            except Exception as e:
                logger.error(f"LLM reasoning error: {e}")
                step2 = ThoughtStep(
                    step_id=2,
                    thought="LLM unavailable, using rule-based fallback",
                    observation=str(e),
                )
                chain.steps.append(step2)
        else:
            step2 = ThoughtStep(
                step_id=2,
                thought="No LLM provider configured, using rule-based reasoning",
                action="rule_based_analysis",
            )
            chain.steps.append(step2)

        decision = await self._make_decision(context, chain)
        chain.conclusion = json.dumps(decision)
        chain.completed_at = datetime.utcnow().isoformat()
        self.reasoning_history.append(chain)
        return chain

    async def _make_decision(self, context: Dict[str, Any], chain: ReasoningChain) -> Dict[str, Any]:
        """Make a trading decision based on reasoning chain."""
        price_change = context.get("price_change_pct", 0)
        volume_spike = context.get("volume_spike", False)
        sentiment = context.get("sentiment_score", 0.5)

        confidence = 0.0
        action = "hold"

        if price_change > 2.0 and volume_spike:
            action = "buy"
            confidence = min(0.9, 0.5 + (price_change / 10) + (0.2 if sentiment > 0.6 else 0))
        elif price_change < -3.0:
            action = "sell"
            confidence = min(0.9, 0.5 + (abs(price_change) / 10))
        elif abs(price_change) < 0.5 and sentiment > 0.7:
            action = "accumulate"
            confidence = 0.4

        return {
            "action": action,
            "confidence": round(confidence, 3),
            "reasoning": f"Price change: {price_change}%, Volume spike: {volume_spike}, Sentiment: {sentiment}",
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def plan_strategy(self, market_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan a sequence of actions based on market state."""
        actions = []
        chain = await self.reason(market_state)

        if chain.conclusion:
            decision = json.loads(chain.conclusion)
            if decision["confidence"] > 0.6:
                actions.append({
                    "type": "trade",
                    "decision": decision,
                    "priority": "high" if decision["confidence"] > 0.8 else "medium",
                })
            actions.append({
                "type": "monitor",
                "interval": 30 if decision.get("action") != "hold" else 60,
            })

        return actions
