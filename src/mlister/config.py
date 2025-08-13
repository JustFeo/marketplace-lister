from __future__ import annotations

import os

from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/mlister"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change")
    MEDIA_ROOT: str = os.getenv(
        "MEDIA_ROOT", os.path.expanduser("~/marketplace-lister/media")
    )
    S3_BUCKET: str | None = os.getenv("S3_BUCKET")
    S3_REGION: str | None = os.getenv("S3_REGION")


settings = Settings()
