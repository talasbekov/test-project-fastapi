from schemas import NamedModel, ReadNamedModel


class FamilyStatusBase(NamedModel):
    pass


class FamilyStatusCreate(FamilyStatusBase):
    pass


class FamilyStatusUpdate(FamilyStatusBase):
    pass


class FamilyStatusRead(FamilyStatusBase, ReadNamedModel):

    class Config:
        orm_mode = True
