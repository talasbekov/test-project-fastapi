from schemas import NamedModel, ReadNamedModel


class InstitutionBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(InstitutionBase):
    pass


class InstitutionRead(InstitutionBase, ReadNamedModel):
    pass
