import uuid
from typing import List, Optional

from pydantic import BaseModel


class HrDocumentStatusBase(BaseModel):
    name: str


class HrDocumentStatusCreate(HrDocumentStatusBase):
    pass


class HrDocumentStatusUpdate(HrDocumentStatusBase):
    pass


class HrDocumentStatusRead(HrDocumentStatusBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True
