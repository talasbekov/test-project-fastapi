from schemas import NamedModel, ReadNamedModel


class FamilyRelationBase(NamedModel):
    family_order: int
    pass


class FamilyRelationCreate(FamilyRelationBase):
    pass


class FamilyRelationUpdate(FamilyRelationBase):
    pass


class FamilyRelationRead(FamilyRelationBase, ReadNamedModel):

    class Config:
        orm_mode = True
