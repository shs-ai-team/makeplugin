from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    backend_name: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()