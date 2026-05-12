from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_sid(self, sid: str):
        stmt = select(Product).where(Product.sid == sid)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, product: Product):
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def create(self, product: Product):
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product