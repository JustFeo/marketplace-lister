from __future__ import annotations

from fastapi import FastAPI

from .routers import items, postings

app = FastAPI(title="Marketplace Lister")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(postings.router, prefix="/postings", tags=["postings"])
