from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from src.database.models_enum import ProductStatus

class ProductSchema(BaseModel):
    id: int
    sid: int
    name: str
    description_of_product: Optional[str] = None
    name_of_ai: Optional[str] = None
    description_ai: Optional[str] = None
    price: Optional[float]
    wholesale_price: Optional[float]
    quantity: Optional[int] = None
    quantity_supplier: Optional[int] = None
    barcode: Optional[str] = None
    status: ProductStatus
    raw_api_data: Optional[dict] = None
    photo_link: Optional[str] = None
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    name: str
    description_of_product: Optional[str]
    name_of_ai: Optional[str]
    description_of_ai: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class AIGenerateResponse(BaseModel):
    before: AIInputData
    after: ProductSchema
    model_config = ConfigDict(from_attributes=True)

class AIInputData(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: Optional[str] = None
    description: Optional[str] = None

class BarcodeParserResponse(BaseModel):
    status: str
    sid: int
    name: str
    price: Decimal
    photo: Optional[str] = None
