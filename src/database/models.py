from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Numeric, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from src.models_enum import ProductStatus

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    sid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    description_of_product: Mapped[Optional[str]] = mapped_column(String(255))
    name_of_ai: Mapped[Optional[str]] = mapped_column(String(50))
    description_ai: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Numeric(10,2))
    wholesale_price: Mapped[float] = mapped_column(Numeric(10,2))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    quantity_supplier: Mapped[int] = mapped_column(Integer, default=0)
    barcode: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), nullable=False, default=ProductStatus.new_product)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())
    raw_api_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    photo_link: Mapped[Optional[str]] = mapped_column(String(100))

