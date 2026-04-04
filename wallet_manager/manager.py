"""Wallet Manager - Unified wallet operations for agents."""
import logging
from typing import Any, Dict, List, Optional
from solana.client import SolanaClient

logger = logging.getLogger(__name__)


class WalletManager:
    """Manages wallet operations across chains."""

    def __init__(self):
        self.solana = SolanaClient()
        self.active_wallet: Optional[str] = None

    def create_wallet(self) -> Dict[str, str]:
        result = self.solana.create_wallet()
        if result.get("status") == "created":
            self.active_wallet = result["public_key"]
        return result

    def import_wallet(self, private_key: str) -> Dict[str, str]:
        result = self.solana.import_wallet(private_key)
        if result.get("status") == "imported":
            self.active_wallet = result["public_key"]
        return result

    def connect_wallet(self, public_key: str) -> Dict[str, str]:
        wallets = self.solana.list_wallets()
        for w in wallets:
            if w["public_key"] == public_key:
                self.active_wallet = public_key
                return {"status": "connected", "public_key": public_key}
        return {"status": "not_found"}

    async def get_balance(self, public_key: str = None) -> Dict[str, Any]:
        key = public_key or self.active_wallet
        if not key:
            return {"error": "No wallet connected"}
        return await self.solana.get_balance(key)

    async def sign_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        if not self.active_wallet:
            return {"error": "No wallet connected"}
        return await self.solana.sign_transaction(self.active_wallet, transaction)

    async def swap_tokens(self, from_token: str, to_token: str, amount: float) -> Dict[str, Any]:
        if not self.active_wallet:
            return {"error": "No wallet connected"}
        return await self.solana.swap_tokens(self.active_wallet, from_token, to_token, amount)

    def wallet_status(self) -> Dict[str, Any]:
        return {
            "active_wallet": self.active_wallet,
            "total_wallets": len(self.solana.list_wallets()),
            "wallets": self.solana.list_wallets(),
        }
