from pydantic import BaseModel, Field
from typing import Optional


class CreateRepoModel(BaseModel):
    name: str
    description: Optional[str] = Field(max_length=255)
    private: Optional[bool] = True

    class Config:
        schema_extra = {
            "example": {
                "name": "ABC",
                "description": "Test Repo",
                "private": True
            }
        }
