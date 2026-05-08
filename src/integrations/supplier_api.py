import httpx
from loguru import logger
from src.core.config import settings
from src.core.constants import all_expends


async def get_item_from_supplier(identifier: str = None)->dict:
    url = f"{settings.SUPPLIER_API3_URL}"
    if not identifier:
        logger.info(f'не передан {identifier}')
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': settings.SUPPLIER_API3_KEY.get_secret_value(),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    params = {}
    if len(identifier) >= 12:
        params['barcodes'] = identifier
    else:
        params['sid'] = identifier
        params['by_sid'] = 'true'
        params['expand'] = all_expends
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            logger.info(response.url)
            if response.status_code != 200:
                logger.error(f'error api {response.status_code}')
            if "text/html" in response.headers.get("Content-Type", ""):
                logger.error("Ошибка: API вернуло HTML страницу вместо JSON. Проверьте SIMALAND_API_URL")
                return None
            data = response.json()
            if isinstance(data, dict):
                items = data.get('items', [])
            elif isinstance(data, list):
                items = data
            else:
                items = []
            return items[0] if items else None
        except Exception as e:
            logger.error(e)
            return None
