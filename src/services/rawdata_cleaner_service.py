from loguru import logger

logger.add("data/logs/rawdata_cleaner.log", rotation="1 week", retention="7 days")


class RawDataCleaner:
    def __init__(self, raw_api_data: dict):
        self.raw_api_data = raw_api_data or {}

    async def clean_data(self, keywords: list[str]) -> dict:
        logger.info(f"получен сырой джейсон: {len(self.raw_api_data)} записей")
        try:
            clean_data = {}
            for key, value in self.raw_api_data.items():
                if any(word.lower() in key.lower() for word in keywords):
                    clean_data[key] = value
            return clean_data
        except Exception as e:
            logger.error(f'Ошибка очистки данных от поставщика: {e}')





