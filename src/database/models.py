from typing import Optional
from sqlalchemy import Integer, String, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from src.database.models_enum import ProductStatus
from src.database.base_model import BaseModel, TimestampMixin

class Product(BaseModel, TimestampMixin):
    sid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    name_of_ai: Mapped[Optional[str]] = mapped_column(String(50))
    description_of_product: Mapped[Optional[str]] = mapped_column(String)
    description_ai: Mapped[Optional[str]] = mapped_column(String)
    price: Mapped[float] = mapped_column(Numeric(10,2))
    wholesale_price: Mapped[float] = mapped_column(Numeric(10,2))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    quantity_supplier: Mapped[int] = mapped_column(Integer, default=0)
    barcode: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), nullable=False, default=ProductStatus.new_product)
    raw_api_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    photo_link: Mapped[Optional[str]] = mapped_column(String)

