import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class StaffDivisionTypeBase(NamedModel):
    pass


class StaffDivisionTypeCreate(StaffDivisionTypeBase):
    pass


class StaffDivisionTypeUpdate(StaffDivisionTypeBase):
    pass


class StaffDivisionTypeRead(StaffDivisionTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True
