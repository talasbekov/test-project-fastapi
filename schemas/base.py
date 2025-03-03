import uuid
import datetime
from typing import Optional, Any, Union, get_origin, get_args

from pydantic import BaseModel, Field, validator, root_validator
from pydantic.schema import Enum

from models import FormEnum, ReserveEnum, ServiceIDStatus


def extract_type(field_type: Any) -> Any:
    origin = get_origin(field_type)
    if origin is Union:
        args = get_args(field_type)
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return non_none[0]
        return None
    return field_type


def default_value(field_name: str, field_type: Any) -> Any:
    base_type = extract_type(field_type)
    lname = field_name.lower()
    # Если тип поля является перечислением, подставляем нужное значение
    if isinstance(base_type, type) and issubclass(base_type, Enum):
        # Для поля form можно вернуть нужное значение, например:
        if field_name.lower() == "form":
            return FormEnum.form2
        if field_name.lower() == "reserve":
            return ReserveEnum.ENLISTED
        if field_name.lower() == "token_status":
            return ServiceIDStatus.RECEIVED
        # Или, если хотите возвращать первый элемент по умолчанию:
        # return list(base_type)[0]

    if base_type == str:
        return "Данные отсутствуют!"
    elif base_type == int:
        return 999999
    elif base_type == float:
        return 999999.0
    elif base_type == datetime.datetime:
        if "to" in lname or "status" in lname or "updated" in lname:
            return datetime.datetime(2025, 1, 1)
        else:
            return datetime.datetime(1920, 1, 1)
    elif base_type == datetime.date:
        if "to" in lname or "status" in lname or "updated" in lname:
            return datetime.date(2025, 1, 1)
        else:
            return datetime.date(1920, 1, 1)
    elif base_type == uuid.UUID:
        return uuid.UUID("00000000-0000-0000-0000-000000000000")
    elif isinstance(base_type, type) and issubclass(base_type, BaseModel):
        return base_type()
    return None


class CustomBaseModel(BaseModel):
    @root_validator(pre=True)
    def replace_nones(cls, values):
        values = dict(values)
        for field_name, field in cls.__fields__.items():
            if values.get(field_name) is None:
                values[field_name] = default_value(field_name, field.outer_type_)
        return values

class Model(CustomBaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NamedModel(Model):
    name: Optional[str]
    nameKZ: Optional[str] = Field(None, nullable=True)

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        values = dict(values)  # Превращаем GetterDict в обычный dict
        values["name"] = values.get("name") or "Данные отсутствуют!"
        values["nameKZ"] = values.get("nameKZ") or "Данные отсутствуют!"
        return values

    class Config:
        from_attributes = True


class TextModel(Model):
    text: str
    textKZ: Optional[str] = Field(None, nullable=True)

    # @validator("text", "textKZ", pre=True, always=True)
    # def default_empty_text(cls, v):
    #     return v if v is not None else "Данные отсутствуют!"

    class Config:
        orm_mode = True


class ReadModel(Model):
    id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    @validator("id", pre=True, always=True)
    def default_uuid(cls, v):
        return v if v is not None else str(uuid.uuid4())

    @validator("created_at", "updated_at", pre=True, always=True)
    def default_date(cls, v):
        return v if v is not None else datetime.datetime(1920, 1, 1)

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
