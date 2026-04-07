from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "customer-service"
    database_url: str = (
        "postgresql+psycopg://msf_user:msf_password@localhost:5432/msf_customer"
    )


settings = Settings()
