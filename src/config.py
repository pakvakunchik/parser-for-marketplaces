from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    SIMALAND_API_URL: str
    SIMALAND_API_KEY: SecretStr
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: SecretStr
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=False
    )

settings = Settings()



