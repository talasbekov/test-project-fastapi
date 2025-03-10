import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Model(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NamedModel(Model):
    name: Optional[str]
    nameKZ: Optional[str] = Field(None, nullable=True)

    class Config:
        from_attributes = True


class TextModel(Model):
    text: str
    textKZ: Optional[str] = Field(None, nullable=True)

    class Config:
        orm_mode = True


class ReadModel(Model):
    id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        # При вызове .dict() или .json() не исключать unset поля
        exclude_unset = False
        # Сериализатор дат в ISO-формат, который понимает Zod
        json_encoders = {datetime.datetime: lambda v: v.isoformat()}


class ReadNamedModel(NamedModel, ReadModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True


class ReadTextModel(TextModel, ReadModel):
    text: Optional[str]
    textKZ: Optional[str]

    class Config:
        orm_mode = True
