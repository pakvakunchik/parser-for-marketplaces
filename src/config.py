import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    SIMALEND_API_URL: str
    SIMALEND_API_KEY: SecretStr
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: SecretStr
    model_config = {'env_file': '.env'}

settings = Settings()
