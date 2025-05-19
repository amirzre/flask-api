from pydantic import BaseModel, ConfigDict, Field


class CreateLog(BaseModel):
    method: str | None = Field(max_length=10, description="Method")
    endpoint: str | None = Field(max_length=255, description="Endpoint address")
    status: str | None = Field(max_length=10, description="Status code")
    user_id: int | None = Field(description="Related user ID")


class LogResponse(BaseModel):
    id: int = Field(examples=[1])
    method: str = Field(examples=["POST"])
    endpoint: str = Field(examples=["/api/v1/users"])
    status: str = Field(examples=["201"])
    user_id: int = Field(examples=[2])

    model_config = ConfigDict(from_attributes=True)
