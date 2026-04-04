#!/usr/bin/env python3
"""Environment Validation - Verify all dependencies and configurations."""
import os
import sys
import json
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = {
    "TELEGRAM_BOT_TOKEN": "Telegram bot token for command interface",
    "SOLANA_RPC_URL": "Solana RPC endpoint URL",
}

OPTIONAL_ENV_VARS = {
    "OPENAI_API_KEY": "OpenAI API key for GPT models",
    "ANTHROPIC_API_KEY": "Anthropic API key for Claude models",
    "FIREWORKS_API_KEY": "Fireworks AI API key",
    "DATABASE_URL": "PostgreSQL connection string",
    "REDIS_URL": "Redis connection string",
    "OLLAMA_URL": "Ollama local LLM endpoint",
}


def check_env_vars() -> dict:
    """Check required and optional environment variables."""
    results = {"required": {}, "optional": {}, "missing_required": []}
    for var, desc in REQUIRED_ENV_VARS.items():
        value = os.getenv(var, "")
        present = bool(value)
        results["required"][var] = {"present": present, "description": desc}
        if not present:
            results["missing_required"].append(var)
    for var, desc in OPTIONAL_ENV_VARS.items():
        value = os.getenv(var, "")
        results["optional"][var] = {"present": bool(value), "description": desc}
    return results


async def check_redis() -> dict:
    """Check Redis connectivity."""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    try:
        import aiohttp
        # Simple TCP check
        host = redis_url.replace("redis://", "").split(":")[0]
        port = int(redis_url.split(":")[-1].split("/")[0]) if ":" in redis_url.replace("redis://", "") else 6379
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=3)
        writer.close()
        await writer.wait_closed()
        return {"status": "connected", "url": redis_url}
    except Exception as e:
        return {"status": "unavailable", "error": str(e), "url": redis_url}


async def check_ollama() -> dict:
    """Check Ollama local LLM."""
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ollama_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m["name"] for m in data.get("models", [])]
                    return {"status": "running", "models": models}
                return {"status": "error", "http_status": resp.status}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


async def check_solana_rpc() -> dict:
    """Check Solana RPC endpoint."""
    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            payload = {"jsonrpc": "2.0", "id": 1, "method": "getHealth"}
            async with session.post(rpc_url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
                return {"status": "connected", "rpc_url": rpc_url, "response": data}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


async def check_database() -> dict:
    """Check PostgreSQL database."""
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        return {"status": "not_configured"}
    try:
        import asyncpg
        conn = await asyncpg.connect(db_url, timeout=5)
        version = await conn.fetchval("SELECT version()")
        await conn.close()
        return {"status": "connected", "version": version}
    except ImportError:
        return {"status": "asyncpg_not_installed"}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


async def run_all_checks() -> dict:
    """Run all environment checks."""
    results = {
        "env_vars": check_env_vars(),
        "redis": await check_redis(),
        "ollama": await check_ollama(),
        "solana_rpc": await check_solana_rpc(),
        "database": await check_database(),
    }

    # Determine overall status
    critical_failures = results["env_vars"]["missing_required"]
    if critical_failures:
        results["overall"] = "FAIL"
        results["message"] = f"Missing required env vars: {', '.join(critical_failures)}"
    else:
        results["overall"] = "PASS"
        results["message"] = "All required checks passed"

    return results


def main():
    print("\n=== Solana Agent Trader - Environment Validation ===\n")
    results = asyncio.run(run_all_checks())

    # Display results
    print("-- Environment Variables --")
    for var, info in results["env_vars"]["required"].items():
        status = "OK" if info["present"] else "MISSING"
        print(f"  [{status}] {var}: {info['description']}")
    print()
    for var, info in results["env_vars"]["optional"].items():
        status = "OK" if info["present"] else "NOT SET"
        print(f"  [{status}] {var}: {info['description']}")

    print(f"\n-- Redis: {results['redis']['status']}")
    print(f"-- Ollama: {results['ollama']['status']}")
    print(f"-- Solana RPC: {results['solana_rpc']['status']}")
    print(f"-- Database: {results['database']['status']}")

    print(f"\n=== Overall: {results['overall']} ===")
    print(f"    {results['message']}\n")

    if results["overall"] == "FAIL":
        print("Set missing environment variables before starting the platform.")
        print("Copy .env.example to .env and fill in values.\n")
        sys.exit(1)

    return results


if __name__ == "__main__":
    main()
