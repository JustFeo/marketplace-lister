from __future__ import annotations

from celery import Celery

from ..config import settings

celery_app = Celery(
    "mlister",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_acks_late = True
celery_app.conf.result_expires = 3600
