import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class HrDocumentStatusBase(NamedModel):
    pass


class HrDocumentStatusCreate(HrDocumentStatusBase):
    pass


class HrDocumentStatusUpdate(HrDocumentStatusBase):
    pass


class HrDocumentStatusRead(HrDocumentStatusBase, ReadNamedModel):

    class Config:
        orm_mode = True
