from schemas import NamedModel, ReadNamedModel


class SurveyTypeBase(NamedModel):
    pass


class SurveyTypeCreate(SurveyTypeBase):
    pass


class SurveyTypeUpdate(SurveyTypeBase):
    pass


class SurveyTypeRead(SurveyTypeBase, ReadNamedModel):
    pass

    class Config:
        orm_mode = True
