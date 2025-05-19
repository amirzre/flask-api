from pydantic import BaseModel, ConfigDict, Field

from src.schemas.filter import BaseFilterParams
from src.utils import PasswordValidator, PhoneValidator


class RegisterUser(BaseModel):
    username: str = Field(max_length=120, description="Username")
    phone: PhoneValidator = Field(description="Phone number")
    password: PasswordValidator = Field(max_length=50, description="Password")


class UpdateUser(BaseModel):
    username: str | None = Field(None, description="Username")
    phone: PhoneValidator | None = Field(None, description="Phone number")
    password: PasswordValidator | None = Field(
        None, max_length=50, description="Password"
    )


class UserResponse(BaseModel):
    id: int = Field(examples=[1])
    username: str = Field(examples=["johndoe"])
    phone: str = Field(examples=["09123456789"])
    created: str = Field(examples=["1404-02-29 11:26:15"])

    model_config = ConfigDict(from_attributes=True)


class UserFilterParams(BaseFilterParams):
    username: str | None = Field(None)
    phone: str | None = Field(None)
    created_from: str | None = Field(None)
    created_to: str | None = Field(None)
