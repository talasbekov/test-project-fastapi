from schemas import NamedModel, ReadNamedModel


class AcademicTitleDegreeBase(NamedModel):
    pass


class AcademicTitleDegreeCreate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeUpdate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeRead(AcademicTitleDegreeBase, ReadNamedModel):

    class Config:
        orm_mode = True
