from schemas import NamedModel, ReadNamedModel


class CandidateCategoryBase(NamedModel):
    pass


class CandidateCategoryCreate(CandidateCategoryBase):
    pass


class CandidateCategoryUpdate(CandidateCategoryBase):
    pass


class CandidateCategoryRead(CandidateCategoryBase, ReadNamedModel):

    class Config:
        orm_mode = True
