from src.exceptions.product_exceptions import ProductNotFoundError
from src.integrations.supplier_api import get_item_from_supplier

async def check_raw_data(barcode: str):
    raw_data = await get_item_from_supplier(barcode)
    if not raw_data:
        raise ProductNotFoundError(barcode)
    return raw_data
