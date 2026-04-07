from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    issuer_uri: str = "https://dev-lc6vtcbv5ll7xa31.eu.auth0.com/"
    customer_service_url: str = "http://localhost:8081/api/customer"
    order_service_url: str = "http://localhost:8082/api/order"
    product_service_url: str = "http://localhost:8083/api/product"
    # Defaults let local dev run without shell exports.
    audience: str | None = Field(
        default="https://dev-lc6vtcbv5ll7xa31.eu.auth0.com/api/v2/"
    )

    @property
    def services(self) -> dict[str, str]:
        return {
            "customer": self.customer_service_url,
            "order": self.order_service_url,
            "product": self.product_service_url,
        }


settings = Settings()
