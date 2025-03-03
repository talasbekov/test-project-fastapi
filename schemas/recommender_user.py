import uuid
from typing import Optional
from pydantic import validator, root_validator

from schemas import Model, ReadModel


class RecommenderUserBase(ReadModel):
    document_link: Optional[str]
    recommendant: Optional[str]
    researcher: Optional[str]
    user_by_id: Optional[str]
    researcher_id: Optional[str]
    user_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        """ Автоматически заменяет None на предустановленные значения """
        values = dict(values)  # Превращаем GetterDict в обычный dict

        defaults = {
            "document_link": "Данные отсутствуют!",
            "recommendant": "Данные отсутствуют!",
            "researcher": "Данные отсутствуют!",
            "user_by_id": str(uuid.uuid4()),
            "researcher_id": str(uuid.uuid4()),
        }

        for key, default_value in defaults.items():
            values[key] = values.get(key) or default_value

        return values


class RecommenderUserCreate(RecommenderUserBase):
    pass


class RecommenderUserUpdate(RecommenderUserBase):
    pass


class RecommenderUserRead(RecommenderUserBase):
    id: Optional[str]

    @validator("user_by_id", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"