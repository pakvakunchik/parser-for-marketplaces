from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Optional[Product] | None:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_sid(self, sid: str) -> Optional[Product] | None:
        query = select(Product).where(Product.sid == sid)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_last_added(self) -> Optional[Product] | None:
        query = select(Product).order_by(desc(Product.created_at)).limit(1)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, product: Product) -> Product:
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update_ai_data(self, product: Product, name_ai: str, description_ai: str) -> Product:
        product.name_of_ai = name_ai
        product.description_ai = description_ai
        self.db.add(product)
        return product

