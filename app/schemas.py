from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title must not be blank")
        return value


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Title must not be blank")
        return value


class Todo(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    title: str
    completed: bool
    created_at: datetime


class TodoStats(BaseModel):
    total: int
    completed: int
    pending: int
