"""API Server - REST API for dashboard and external integrations."""
import asyncio
import json
import logging
from typing import Any, Dict
from aiohttp import web
from agents.runtime import AgentRuntime
from trading_engine.market_data import MarketDataService
from trading_engine.signals import SignalGenerator
from trading_engine.strategy_manager import StrategyManager
from trading_engine.executor import TradeExecutor
from trading_engine.position_manager import PositionManager
from backtesting.engine import BacktestEngine
from wallet_manager.manager import WalletManager
from llm_providers.router import ModelRouter
from skills.registry.crawler import RepositoryCrawler

logger = logging.getLogger(__name__)

# Global state
runtime = AgentRuntime()
market_data = MarketDataService()
signal_gen = SignalGenerator()
strategy_mgr = StrategyManager()
executor = TradeExecutor(mode="simulation")
position_mgr = PositionManager()
backtest = BacktestEngine()
wallet_mgr = WalletManager()
model_router = ModelRouter()
crawler = RepositoryCrawler()


async def handle_status(request):
    return web.json_response({
        "status": "online",
        "agents": runtime.get_runtime_status(),
        "strategies": strategy_mgr.list_strategies(),
        "positions": position_mgr.get_stats(),
        "wallets": wallet_mgr.wallet_status(),
    })


async def handle_agents(request):
    return web.json_response({"agents": runtime.list_agents()})


async def handle_create_agent(request):
    data = await request.json()
    agent_id = data.get("agent_id", f"agent_{len(runtime.agents)+1}")
    config = data.get("config", {})
    agent = runtime.create_agent(agent_id, config)
    return web.json_response({"created": agent.get_status()})


async def handle_start_agents(request):
    await runtime.start_all()
    return web.json_response(runtime.get_runtime_status())


async def handle_stop_agents(request):
    await runtime.stop_all()
    return web.json_response(runtime.get_runtime_status())


async def handle_market_data(request):
    symbol = request.query.get("symbol", "SOL/USD")
    price = await market_data.get_price(symbol)
    ticker = await market_data.get_ticker(symbol)
    return web.json_response({"price": price, "ticker": ticker})


async def handle_signals(request):
    symbol = request.query.get("symbol", "SOL/USD")
    ohlcv = await market_data.get_ohlcv(symbol, limit=50)
    prices = [c["close"] for c in ohlcv]
    signals = signal_gen.generate_signals(prices, symbol)
    return web.json_response({"signals": signals})


async def handle_strategies(request):
    return web.json_response({"strategies": strategy_mgr.list_strategies()})


async def handle_backtest(request):
    data = await request.json() if request.method == "POST" else {}
    strategy = data.get("strategy", request.query.get("strategy", "momentum"))
    days = int(data.get("days", request.query.get("days", 365)))
    result = backtest.run_backtest(strategy=strategy, days=days)
    return web.json_response(result)


async def handle_positions(request):
    return web.json_response({
        "positions": position_mgr.list_positions(),
        "stats": position_mgr.get_stats(),
    })


async def handle_orders(request):
    return web.json_response({"orders": executor.get_history()})


async def handle_create_wallet(request):
    result = wallet_mgr.create_wallet()
    return web.json_response(result)


async def handle_wallet_status(request):
    return web.json_response(wallet_mgr.wallet_status())


async def handle_skills(request):
    local_skills = crawler.crawl_local_skills("skills")
    return web.json_response(crawler.export_registry())


async def handle_health(request):
    return web.json_response({
        "status": "healthy",
        "agents": len(runtime.agents),
        "skills": len(crawler.discovered_skills),
    })


async def handle_simulation_data(request):
    """Return simulation data for 3D dashboard visualization."""
    agents_data = []
    for aid, agent in runtime.agents.items():
        status = agent.get_status()
        agents_data.append({
            "id": aid,
            "status": status["status"],
            "x": hash(aid) % 100 - 50,
            "y": hash(aid + "y") % 100 - 50,
            "z": hash(aid + "z") % 100 - 50,
            "connections": [other for other in runtime.agents if other != aid],
        })

    prices = []
    for _ in range(100):
        p = await market_data.get_price("SOL/USD")
        prices.append(p["price"])

    return web.json_response({
        "agents": agents_data,
        "prices": prices,
        "stats": position_mgr.get_stats(),
        "orders": executor.get_history(20),
    })


def create_app() -> web.Application:
    app = web.Application()

    # CORS middleware
    @web.middleware
    async def cors_middleware(request, handler):
        if request.method == "OPTIONS":
            response = web.Response()
        else:
            response = await handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    app.middlewares.append(cors_middleware)

    # Routes
    app.router.add_get("/api/status", handle_status)
    app.router.add_get("/api/health", handle_health)
    app.router.add_get("/api/agents", handle_agents)
    app.router.add_post("/api/agents", handle_create_agent)
    app.router.add_post("/api/agents/start", handle_start_agents)
    app.router.add_post("/api/agents/stop", handle_stop_agents)
    app.router.add_get("/api/market", handle_market_data)
    app.router.add_get("/api/signals", handle_signals)
    app.router.add_get("/api/strategies", handle_strategies)
    app.router.add_get("/api/backtest", handle_backtest)
    app.router.add_post("/api/backtest", handle_backtest)
    app.router.add_get("/api/positions", handle_positions)
    app.router.add_get("/api/orders", handle_orders)
    app.router.add_post("/api/wallet/create", handle_create_wallet)
    app.router.add_get("/api/wallet/status", handle_wallet_status)
    app.router.add_get("/api/skills", handle_skills)
    app.router.add_get("/api/simulation", handle_simulation_data)

    return app


def start_server(host: str = "0.0.0.0", port: int = 8080):
    """Start the API server."""
    app = create_app()
    logger.info(f"Starting API server on {host}:{port}")
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_server()
