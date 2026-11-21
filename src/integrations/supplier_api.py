from typing import Optional

import httpx
from loguru import logger

from src.core.config import settings
from src.core.constants import all_expends


async def get_item_from_supplier(identifier: Optional[str] = None) -> Optional[dict]:
    if not identifier:
        logger.info(f'Не передан идентификатор товара (barcode или sid)')
        return None
    code = str(identifier).strip()
    if not code:
        return None
    url = settings.api.SUPPLIER_API3_URL
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': settings.api.SUPPLIER_API3_KEY.get_secret_value(),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    params: dict[str, str] = {}
    if len(code) >= 12:
        params['barcodes'] = code
    else:
        params['sid'] = code
        params['by_sid'] = 'true'
        params['expand'] = all_expends
    async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            logger.info(f"Запрос к поставщику: {response.url} -> {response.status_code}")
            if response.status_code != 200:
                logger.error(f'error api {response.status_code}')
            if "text/html" in response.headers.get("Content-Type", ""):
                logger.error("API поставщика вернуло HTML вместо JSON. Проверьте SUPPLIER_API3_URL")
                return None
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                items = data.get('items') or []
            elif isinstance(data, list):
                items = data
            else:
                items = []
            return items[0] if items else None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка API поставщика {e.response.status_code}: {e.response.text[:300]}")
            return None
        except Exception as e:
            logger.error(f'Ошибка при запросе к API поставщика: {e}')
            return None
