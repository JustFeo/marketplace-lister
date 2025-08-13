from __future__ import annotations

from typing import Any, Dict

from ..adapters.base import MarketplaceAdapter, MockAdapter

_ADAPTERS = {
    "mock": MockAdapter,
    "ebay": MockAdapter,  # placeholder
    "etsy": MockAdapter,  # placeholder
    "marktplaats": MockAdapter,  # placeholder
}


def get_adapter(name: str, credentials: Dict[str, Any]) -> MarketplaceAdapter:
    key = name.lower()
    adapter_cls = _ADAPTERS.get(key)
    if not adapter_cls:
        raise ValueError(f"No adapter registered for marketplace '{name}'")
    return adapter_cls(credentials)
