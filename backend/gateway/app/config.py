from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # Required (no defaults, must exist in .env or env vars)
    issuer_uri: str
    audience: str
    customer_service_url: str

    @property
    def services(self) -> dict[str, str]:
        return {
            "customer": self.customer_service_url,
        }


settings = Settings()
