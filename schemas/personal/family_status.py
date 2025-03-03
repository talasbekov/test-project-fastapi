from schemas import NamedModel,  ReadModel


class FamilyStatusBase(NamedModel):
    pass


class FamilyStatusCreate(FamilyStatusBase):
    pass


class FamilyStatusUpdate(FamilyStatusBase):
    pass


class FamilyStatusRead(ReadModel, NamedModel):

    class Config:
        orm_mode = True
