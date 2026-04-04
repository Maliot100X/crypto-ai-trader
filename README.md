# Solana Agent Trader

## Self-Assembling AI Trading Lab

A complete autonomous AI trading platform that assembles itself from external repositories and skill registries. Multi-agent runtime with LLM reasoning, blockchain interaction, and real-time 3D visualization.

```
    ____        __                        ___                    __     ______               __
   / __/____   / /____ _ ____   ____ _   /   |  ____ _ ___     / /_   /_  __/_____ ____ _ _/ /___   _____
  \__ \/ __ \ / // __ `// __ \ / __ `/  / /| | / __ `// _ \   / __/    / /  / ___// __ `// __  / _ \/ ___/
 ___/ / /_/ // // /_/ // / / // /_/ /  / ___ |/ /_/ //  __/  / /_     / /  / /   / /_/ // /_/ //  __/ /
/____/\____//_/ \__,_//_/ /_/ \__,_/  /_/  |_|\__, / \___/   \__/    /_/  /_/    \__,_/ \__,_/ \___/_/
                                              /____/
```

---

## Architecture

```
+---------------------------------------------------+
|           SOLANA AGENT TRADER PLATFORM             |
+---------------------------------------------------+
|                                                     |
|  +----------+  +----------+  +----------+          |
|  | Agent    |  | Agent    |  | Agent    |  ...     |
|  | Alpha    |  | Beta     |  | Gamma    |          |
|  +----+-----+  +----+-----+  +----+-----+          |
|       |              |              |                |
|  +----v--------------v--------------v-----+         |
|  |         AGENT RUNTIME                   |         |
|  |  Brain | Memory | Skills | Tools        |         |
|  +----+--------------------------------+--+         |
|       |                                |             |
|  +----v---------+  +---------v--------+             |
|  | LLM Providers|  | Trading Engine   |             |
|  | Ollama       |  | Signals          |             |
|  | OpenAI       |  | Strategies       |             |
|  | Anthropic    |  | Risk Manager     |             |
|  | Fireworks    |  | Executor         |             |
|  +--------------+  +--------+---------+             |
|                             |                        |
|  +----------+  +------------v-------+               |
|  | Telegram |  | Solana Blockchain  |               |
|  | Bot      |  | Wallet Manager     |               |
|  +----------+  | DEX Trading        |               |
|                 +--------------------+               |
|                                                     |
|  +-------------------+  +-------------------+       |
|  | Backtesting       |  | 3D Dashboard      |       |
|  | Engine            |  | (Next.js/Three.js)|       |
|  +-------------------+  +-------------------+       |
+---------------------------------------------------+
```

---

## Features

### Multi-Agent Runtime
- Autonomous trading agents with LLM-powered reasoning
- Each agent: Brain, Memory, SkillLoader, ToolRegistry
- Async execution with configurable personalities
- Agent-to-agent interaction network

### LLM Provider Layer
- **Ollama** - Local LLM runtime
- **OpenAI** - GPT models
- **Anthropic** - Claude models
- **Fireworks AI** - High-speed inference (Kimi K2.5 Turbo)
- Automatic failover and model routing

### Trading Engine
- Market data service (real-time + historical)
- Technical indicators: RSI, MACD, Bollinger Bands, SMA, EMA
- Strategy manager: Momentum, Mean Reversion, AI Signals, Sentiment, Arbitrage
- Risk manager: Position sizing, stop-loss, take-profit, drawdown limits
- Trade executor (simulation + live modes)
- Position tracking with P&L

### Backtesting Engine
- Historical strategy backtesting
- Metrics: ROI, Sharpe ratio, max drawdown, win rate
- Multiple strategy support
- Trade log generation

### Solana Blockchain
- Wallet creation and import
- Balance monitoring
- Transaction signing
- DEX token swaps (Jupiter-compatible)

### Telegram Bot
Commands: `/help`, `/models`, `/start_agents`, `/stop_agents`, `/list_agents`, `/create_wallet`, `/connect_wallet`, `/wallet_status`, `/run_backtest`, `/deploy_strategy`, `/system_status`, `/logs`

### 3D Dashboard
- Next.js + Three.js + WebGL
- Animated particle field background
- Agent nodes in 3D network visualization
- Orbital rings and data streams
- Real-time trading activity display
- Strategy performance metrics
- Vercel-ready deployment

### Self-Assembling Skill System
- Dynamic skill discovery from repositories
- SKILL.md / skill.json parsing
- Runtime skill registration
- 9+ external repository crawling configured
- Skills.sh and CryptoSkill.org registry integration

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/Maliot100X/crypto-ai-trader.git
cd crypto-ai-trader
bash scripts/install.sh
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Verify Environment

```bash
python verify_env.py
```

### 4. Run Tests

```bash
python -m unittest tests.test_platform -v
```

### 5. Start the Platform

```bash
# Start API server
python api_server.py

# Start dashboard (in another terminal)
cd dashboard && npm run dev

# Or use Docker
cd docker && docker-compose up
```

---

## Project Structure

```
/agents              - Multi-agent runtime system
  brain.py           - LLM-powered reasoning engine
  memory.py          - Working + long-term memory
  skill_loader.py    - Dynamic skill discovery
  tool_registry.py   - Tool registration and invocation
  runtime.py         - Agent lifecycle management

/llm_providers       - LLM provider abstraction layer
  provider.py        - Base provider interface
  ollama_provider.py - Local Ollama integration
  openai_provider.py - OpenAI API
  anthropic_provider.py - Anthropic Claude API
  fireworks_provider.py - Fireworks AI
  router.py          - Auto model routing with failover

/trading_engine      - Modular trading infrastructure
  market_data.py     - Price feeds and OHLCV data
  signals.py         - Technical indicator signals
  strategy_manager.py - Strategy orchestration
  risk_manager.py    - Risk controls and position sizing
  executor.py        - Trade order execution
  position_manager.py - Open position tracking

/backtesting         - Strategy backtesting engine
  engine.py          - Historical simulation with metrics

/solana              - Blockchain interaction layer
  client.py          - Solana RPC client

/wallet_manager      - Multi-chain wallet operations
  manager.py         - Unified wallet interface

/telegram_bot        - Telegram command interface
  controller.py      - Bot handlers and commands

/skills              - Skill modules and registry
  /registry          - Skill discovery and crawling

/simulation          - Trading simulation engine
  simulator.py       - Full multi-agent simulation

/dashboard           - Next.js 3D monitoring dashboard
  /src/components    - Scene3D, Dashboard components
  /src/app           - Next.js app router pages

/docker              - Docker orchestration
/scripts             - Installation and setup scripts
/tests               - Comprehensive test suite
```

---

## Docker Deployment

```bash
cd docker
docker-compose up -d
```

Services:
- **agent-runtime** (port 8080) - API + agent execution
- **dashboard** (port 3000) - Next.js 3D dashboard
- **telegram-bot** - Command interface
- **postgres** (port 5432) - Database
- **redis** (port 6379) - Cache
- **ollama** (port 11434) - Local LLM

---

## Vercel Deployment (Dashboard)

The dashboard is ready for Vercel deployment:

```bash
cd dashboard
npx vercel
```

Set the environment variable:
- `NEXT_PUBLIC_API_URL` = your API server URL

---

## LLM Configuration

### Fireworks AI (Recommended)
```
base_url=https://api.fireworks.ai/inference/v1
model=accounts/fireworks/routers/kimi-k2p5-turbo
```

### Ollama (Local)
```bash
ollama pull llama3
ollama serve
```

---

## External Repository Integration

The platform crawls and integrates skills from:

| Repository | Category |
|---|---|
| solana-foundation/awesome-solana-ai | Solana AI Tools |
| VoltAgent/awesome-openclaw-skills | OpenClaw Skills |
| sundial-org/awesome-openclaw-skills | OpenClaw Skills |
| mvanhorn/last30days-skill | OpenClaw Skills |
| mergisi/awesome-openclaw-agents | Agent Frameworks |
| Panniantong/Agent-Reach | Agent Framework |
| affaan-m/everything-claude-code | AI Coding |
| obra/superpowers | AI Orchestration |
| evan-kolberg/prediction-market-backtesting | Backtesting |

---

## Test Results

```
Ran 32 tests in 0.020s - OK

- AgentBrain:      3/3 passed
- AgentRuntime:    3/3 passed
- Backtesting:     2/2 passed
- MemoryStore:     4/4 passed
- SkillLoader:     3/3 passed
- SkillRegistry:   2/2 passed
- TelegramBot:     2/2 passed
- ToolRegistry:    2/2 passed
- TradingEngine:   8/8 passed
- WalletManager:   3/3 passed
```

---

## License

MIT License
