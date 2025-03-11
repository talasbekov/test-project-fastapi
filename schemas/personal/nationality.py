from typing import Optional

from schemas import NamedModel

class NationalityBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NationalityCreate(NationalityBase):
    pass

class NationalityUpdate(NationalityBase):
    pass

class NationalityRead(NationalityBase):
    id: Optional[str]
