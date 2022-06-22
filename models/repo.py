from pydantic import BaseModel, Field
from typing import Optional, List


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


class UpdateTopicsModel(BaseModel):
    repo_name: str
    username: Optional[str] = None
    topics: List[str]

    class Config:
        schema_extra = {
            "example": {
                "repo_name": "ABC",
                "topics": ["python", "fastapi"]
            }
        }
