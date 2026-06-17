import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from src.integrations.ai.prompts import prompt
from src.core.config import settings
from loguru import logger

from src.services.rawdata_cleaner_service import RawDataCleaner

logger.add('data/logs/githubAI.log', rotation='10 MB', encoding='utf-8', level='DEBUG')
load_dotenv()

client = AsyncOpenAI(
    base_url=settings.api.GITHUB_API_BASE_URL,
    api_key=settings.api.GITHUB_API_AI_TOKEN.get_secret_value(),
    timeout=settings.api.GITHUB_API_TIMEOUT
)
class AiGenerator:
    def __init__(self, clean_data):
        self.clean_data = clean_data

    @staticmethod
    async def generate_name_and_description(clean_data) -> dict:
        if not clean_data:
            logger.info(" СТОП: raw_data пустая или равна None!")
            return {
                "name": "Ошибка: у товара нет сырых данных для ИИ",
                "description": "Пожалуйста, заполните raw_api_data"
            }
        if hasattr(clean_data, 'model_dump_json'):
            prompt_input = clean_data.model_dump_json(exclude_unset=True)
        else:
            prompt_input = json.dumps(clean_data, ensure_ascii=False)
        final_prompt = str(prompt(prompt_input))
        logger.info(f"--- ОТПРАВКА В ГИТХАБ AI ---")
        logger.info(f"Тип данных: {type(prompt_input)}")
        logger.info(f"Текст промпта: {str(prompt_input)[:200]}...")
        try:
            response = await client.chat.completions.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": final_prompt}],
                response_format={'type': 'json_object'},
                temperature=0.7,
            )
            raw_json_string = response.choices[0].message.content
            logger.info(f'сырой ответ от ии {raw_json_string[::]}')
            try:
                ai_data = json.loads(raw_json_string)
                return {
                    "name": ai_data.get("name", "Без названия"),
                    "description": ai_data.get("description", "Без описания")
                }
            except (json.JSONDecodeError, TypeError):
                return {
                    'name': 'Ошибка генерации названия',
                    'description': 'Не удалось распарсить ответ от ИИ'
                }
        except Exception as e:
            logger.error(f" Ошибка при запросе к GitHub API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Тело ответа: {e.response.text[:500]}")
            return {'name': 'Ошибка генерации',
            'description': f'GitHub API вернул ошибку: {str(e)}'
        }



