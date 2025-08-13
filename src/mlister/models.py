from __future__ import annotations

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="EUR")
    quantity = Column(Integer, default=1)
    category = Column(Text)
    condition = Column(Text)
    location = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="items")
    images = relationship(
        "ItemImage", back_populates="item", cascade="all, delete-orphan"
    )


class ItemImage(Base):
    __tablename__ = "item_images"
    id = Column(UUID(as_uuid=True), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"))
    filename = Column(Text, nullable=False)
    url = Column(Text)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="images")


class Marketplace(Base):
    __tablename__ = "marketplaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    has_api = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MarketplaceAccount(Base):
    __tablename__ = "marketplace_accounts"
    id = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"))
    account_name = Column(Text)
    api_key = Column(Text)
    api_secret = Column(Text)
    oauth_token = Column(Text)
    oauth_refresh = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Posting(Base):
    __tablename__ = "postings"
    id = Column(UUID(as_uuid=True), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"))
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"))
    account_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_accounts.id"))
    marketplace_listing_id = Column(Text)
    status = Column(Text, nullable=False)
    last_error = Column(Text)
    attempt_count = Column(Integer, default=0)
    scheduled_at = Column(DateTime(timezone=True))
    posted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PostingLog(Base):
    __tablename__ = "posting_logs"
    id = Column(UUID(as_uuid=True), primary_key=True)
    posting_id = Column(
        UUID(as_uuid=True), ForeignKey("postings.id", ondelete="CASCADE")
    )
    event = Column(Text)
    details = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
