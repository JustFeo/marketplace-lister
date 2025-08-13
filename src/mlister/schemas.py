from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: str
    price: float
    currency: str = "EUR"
    quantity: int = 1
    category: Optional[str] = None
    condition: Optional[str] = None
    location: Optional[str] = None


class ItemOut(ItemCreate):
    id: str

    class Config:
        from_attributes = True


class PostingCreate(BaseModel):
    item_id: str
    marketplace_ids: List[int]
    schedule_at: Optional[str] = None


class PostingOut(BaseModel):
    id: str
    status: str
    marketplace_listing_id: Optional[str] = None
    last_error: Optional[str] = None

    class Config:
        from_attributes = True
