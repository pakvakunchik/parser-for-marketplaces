from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=False
    )

class DBSettings(ConfigBaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')
    URL: str
    USER: str
    PASSWORD: str
    HOST: str
    NAME: str
    PORT: str

class ApiSettings(ConfigBaseSettings):
    SUPPLIER_API5_URL: str
    SUPPLIER_API5_KEY: SecretStr
    SUPPLIER_API3_URL: str
    SUPPLIER_API3_KEY: SecretStr
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: SecretStr
    GITHUB_API_AI_TOKEN: SecretStr
    GITHUB_API_BASE_URL: str
    GITHUB_API_TIMEOUT: int = 60

class EngineSettings(ConfigBaseSettings):
    model_config = SettingsConfigDict(env_prefix='POOL_')
    SIZE: int = 5
    MAX_OVERFLOW: int = 10
    TIMEOUT: int = 30
    RECYCLE: int = 1800

class Settings(ConfigBaseSettings):
    db: DBSettings = DBSettings()
    engine: EngineSettings = EngineSettings()
    api: ApiSettings = ApiSettings()

settings = Settings()



