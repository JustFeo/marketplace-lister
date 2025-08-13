from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Item, ItemImage
from ..schemas import ItemCreate, ItemOut
from ..utils.images import save_image_variants

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ItemOut])
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items


@router.post("/", response_model=ItemOut)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    itm = Item(
        id=uuid.uuid4(),
        title=payload.title,
        description=payload.description,
        price=payload.price,
        currency=payload.currency,
        quantity=payload.quantity,
        category=payload.category,
        condition=payload.condition,
        location=payload.location,
    )
    db.add(itm)
    db.commit()
    db.refresh(itm)
    return itm


@router.post("/{item_id}/images")
async def upload_image(
    item_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    itm = db.get(Item, item_id)
    if not itm:
        raise HTTPException(status_code=404, detail="item not found")
    img_id = str(uuid.uuid4())
    tmp_path = f"/tmp/{img_id}_{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    paths = save_image_variants(None, item_id, img_id, tmp_path)
    img = ItemImage(
        id=uuid.uuid4(),
        item_id=itm.id,
        filename=file.filename,
        url=paths["orig"],
        width=None,
        height=None,
    )
    db.add(img)
    db.commit()
    return {"id": str(img.id), "url": img.url}
