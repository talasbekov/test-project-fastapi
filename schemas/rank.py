from typing import Optional, List

from pydantic import AnyUrl, root_validator, validator

from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class RankBase(NamedModel):
    rank_order: int
    military_url: AnyUrl
    employee_url: AnyUrl


class RankCreate(RankBase):
    military_url: Optional[AnyUrl]
    employee_url: Optional[AnyUrl]


class RankUpdate(RankBase):
    name: Optional[str]
    nameKZ: Optional[str]
    rank_order: Optional[int]
    military_url: Optional[AnyUrl]
    employee_url: Optional[AnyUrl]

    @validator("military_url", "employee_url", pre=True, always=True)
    def default_url(cls, v):
        return v or "https://default.url"


class RankRead(RankBase, ReadNamedModel):
    rank_order: Optional[int] = 999999
    military_url: Optional[str] = "Данные отсутствуют!"
    employee_url: Optional[str] = "Данные отсутствуют!"

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        # Превращаем GetterDict в обычный dict
        values = dict(values)

        values["rank_order"] = values.get("rank_order") or 999999
        values["military_url"] = values.get("military_url") or "Данные отсутствуют!"
        values["employee_url"] = values.get("employee_url") or "Данные отсутствуют!"

        return values


class RankPaginationRead(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[RankRead]]