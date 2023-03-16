import uuid
from typing import List, Optional

from pydantic import BaseModel


class HrDocumentStatusBase(BaseModel):
    name_kz: str
    name_ru: str


class HrDocumentStatusCreate(HrDocumentStatusBase):
    pass


class HrDocumentStatusUpdate(HrDocumentStatusBase):
    pass


class HrDocumentStatusRead(HrDocumentStatusBase):
    id: Optional[uuid.UUID]
    name_kz: Optional[str]
    name_ru: Optional[str]

    class Config:
        orm_mode = True
