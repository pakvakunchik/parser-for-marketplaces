from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product
from src.repositories.product_repository import ProductRepository
from src.services.photo_service import get_photo
from src.services.supplier_services import check_raw_data


def _safe_float(value, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProductRepository(db)

    async def upsert_by_code(self, barcode: str):
        raw_data = await check_raw_data(barcode)
        sid = raw_data.get("sid")
        if not sid:
            raise ValueError(f"В данных от поставщика нет sid: {raw_data}")

        photo_url = await get_photo(raw_data)
        existing_product = await self.repo.get_by_sid(int(sid))

        if existing_product:
            existing_product.quantity += 1
            if photo_url and not existing_product.photo_link:
                existing_product.photo_link = photo_url
            product = await self.repo.update(existing_product)
            logger.info(f"Товар {product.sid} ({product.name}) обновлён, кол-во: {product.quantity}")
        else:
            product = Product(
                sid=int(sid),
                name=(raw_data.get("name") or "")[:255],
                description_of_product=raw_data.get("description"),
                price=_safe_float(raw_data.get("price"), 0.0),
                wholesale_price=_safe_float(raw_data.get("wholesale_price"), 0.0),
                barcode=barcode,
                raw_api_data=raw_data,
                quantity_supplier=int(raw_data.get("balance") or 0),
                quantity=1,
                photo_link=photo_url,
            )
            product = await self.repo.create(product)
            logger.info(f"Добавлен новый товар {product.sid} ({product.name})")

        return product

