from __future__ import annotations

import asyncio
from typing import Any, Dict


class MarketplaceAdapter:
    def __init__(self, credentials: Dict[str, Any]):
        self.credentials = credentials

    async def create_listing(self, item: dict, images: list) -> dict:
        raise NotImplementedError

    async def update_listing(self, listing_id: str, item: dict, images: list) -> dict:
        raise NotImplementedError

    async def delete_listing(self, listing_id: str) -> bool:
        raise NotImplementedError

    async def get_listing_status(self, listing_id: str) -> dict:
        raise NotImplementedError


class MockAdapter(MarketplaceAdapter):
    async def create_listing(self, item: dict, images: list) -> dict:
        await asyncio.sleep(0.1)
        return {
            "marketplace_listing_id": "mock-" + item["id"],
            "url": "https://example.com/mock",
        }

    async def update_listing(self, listing_id: str, item: dict, images: list) -> dict:
        await asyncio.sleep(0.05)
        return {"ok": True}

    async def delete_listing(self, listing_id: str) -> bool:
        await asyncio.sleep(0.05)
        return True

    async def get_listing_status(self, listing_id: str) -> dict:
        await asyncio.sleep(0.05)
        return {"status": "posted"}
