from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.product_repository import ProductRepository
from src.services.supplier_services import check_raw_data
from src.database.models import Product
from src.services.photo_service import get_photo

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProductRepository(db)

    async def upsert_by_code(self, barcode: str):
        raw_data = await check_raw_data(barcode)
        sid = raw_data.get('sid')
        if not sid:
            raise ValueError(f"В данных от поставщика нет sid: {raw_data}")
        existing_product = await self.repo.get_by_sid(sid)
        if existing_product:
            existing_product.quantity += 1
            product = await self.repo.update(existing_product)
            logger.info(f'Товар {product.sid, product.name} обновлён')
        else:
            product = Product(
                sid=sid,
                name=raw_data.get('name', '')[:50],
                price=float(raw_data.get('price', 0)),
                wholesale_price=float(raw_data.get('wholesale_price')),
                barcode=barcode,
                raw_api_data=raw_data,
                quantity_supplier=raw_data.get('balance', 0),
                quantity=1,
                photo_link=raw_data.get('photoUrl', None)
            )
            product = await self.repo.create(product)
        await get_photo(raw_data)
        return product

