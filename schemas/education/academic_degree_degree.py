from schemas import NamedModel, ReadNamedModel


class AcademicDegreeDegreeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AcademicDegreeDegreeCreate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeUpdate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeRead(AcademicDegreeDegreeBase, ReadNamedModel):
    pass
