from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.database.models_enum import ProductStatus

class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description_of_product: Optional[str]
    name_of_ai: Optional[str]
    description_of_ai: Optional[str]
    price: Optional[float]
    wholesale_price: Optional[float]
    quantity: Optional[int]
    quantity_supplier: Optional[int]
    barcode: Optional[str]
    status: ProductStatus
    raw_api_data: Optional[dict] = None
    updated_at: Optional[datetime]
    created_at: Optional[datetime]


