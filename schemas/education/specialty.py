from schemas import NamedModel, ReadNamedModel


class SpecialtyBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(SpecialtyBase):
    pass


class SpecialtyRead(SpecialtyBase, ReadNamedModel):
    pass
