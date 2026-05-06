from openai import OpenAI
from dotenv import load_dotenv
from src.integrations.ai.prompts import generate_product_description
from src.core.config import settings

load_dotenv()

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY.get_secret_value(),
    base_url=settings.OPENROUTER_BASE_URL,
)

user_content = generate_product_description()
resp = client.chat.completions.create(
    model="openrouter/free",
    messages=[{"role": "user", "content": str(user_content)}] #type: ignore
)

