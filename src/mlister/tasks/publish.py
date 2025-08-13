from __future__ import annotations

import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Item, ItemImage, Marketplace, Posting
from ..services.factory import get_adapter
from ..tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=5)
def publish_posting(self, posting_id: str) -> None:
    db: Session = SessionLocal()
    try:
        posting: Posting | None = db.get(Posting, posting_id)
        if not posting:
            return
        item: Item | None = db.get(Item, posting.item_id)
        market: Marketplace | None = db.get(Marketplace, posting.marketplace_id)
        images = db.query(ItemImage).filter(ItemImage.item_id == item.id).all()

        if not item or not market:
            posting.status = "failed"
            posting.last_error = "Missing item or marketplace"
            db.commit()
            return

        # mock credentials for now
        adapter = get_adapter(market.name, credentials={})

        async def _run():
            res = await adapter.create_listing(
                item={"id": str(item.id), "title": item.title},
                images=[i.url for i in images],
            )
            return res

        res = asyncio.run(_run())
        posting.marketplace_listing_id = res.get("marketplace_listing_id")
        posting.status = "posted"
        posting.posted_at = datetime.utcnow()
        posting.attempt_count = (posting.attempt_count or 0) + 1
        db.commit()
    except Exception as exc:  # noqa: BLE001
        posting = db.get(Posting, posting_id)
        if posting:
            posting.status = "failed"
            posting.last_error = str(exc)
            posting.attempt_count = (posting.attempt_count or 0) + 1
            db.commit()
        raise self.retry(exc=exc, countdown=min(60, 2**self.request.retries))
    finally:
        db.close()
