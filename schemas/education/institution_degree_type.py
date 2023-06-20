from schemas import NamedModel, ReadNamedModel


class InstitutionDegreeTypeBase(NamedModel):
    pass


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True
