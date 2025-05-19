from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(description="Username")
    password: str = Field(description="Password")


class LoginResponse(BaseModel):
    id: int = Field(examples=[1])
    username: str = Field(examples=["johndoe"])

    model_config = ConfigDict(from_attributes=True)
