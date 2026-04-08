from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Required (no defaults, must exist in .env or env vars)
    app_name: str
    database_url: str


settings = Settings()
