from schemas import NamedModel, ReadNamedModel


class QuestionTypeBase(NamedModel):
    pass


class QuestionTypeCreate(QuestionTypeBase):
    pass


class QuestionTypeUpdate(QuestionTypeBase):
    pass


class QuestionTypeRead(QuestionTypeBase, ReadNamedModel):
    pass

    class Config:
        orm_mode = True
