from __future__ import annotations

import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Item, Marketplace, Posting
from ..schemas import PostingCreate, PostingOut
from ..tasks.publish import publish_posting

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[PostingOut])
def list_postings(db: Session = Depends(get_db)):
    return db.query(Posting).all()


@router.post("/", response_model=PostingOut)
def create_postings(payload: PostingCreate, db: Session = Depends(get_db)):
    item = db.get(Item, payload.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    last_posting = None
    for mid in payload.marketplace_ids:
        market = db.get(Marketplace, mid)
        if not market:
            raise HTTPException(status_code=404, detail=f"marketplace {mid} not found")
        posting = Posting(
            id=uuid.uuid4(),
            item_id=item.id,
            marketplace_id=market.id,
            status="pending",
            scheduled_at=None,
            created_at=datetime.utcnow(),
        )
        db.add(posting)
        db.commit()
        publish_posting.delay(str(posting.id))
        last_posting = posting
    return last_posting


@router.get("/{posting_id}", response_model=PostingOut)
def get_posting(posting_id: str, db: Session = Depends(get_db)):
    p = db.get(Posting, posting_id)
    if not p:
        raise HTTPException(status_code=404, detail="not found")
    return p
