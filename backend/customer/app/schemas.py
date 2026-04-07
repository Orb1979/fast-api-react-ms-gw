from pydantic import BaseModel, ConfigDict, Field


class CustomerCreateUpdate(BaseModel):
    name: str
    email: str | None = None
    phone_number: str | None = Field(default=None, alias="phoneNumber")

    model_config = ConfigDict(populate_by_name=True)


class CustomerRead(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone_number: str | None = Field(default=None, alias="phoneNumber")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
