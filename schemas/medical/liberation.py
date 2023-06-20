from schemas import NamedModel, ReadNamedModel


class LiberationBase(NamedModel):
    pass


class LiberationCreate(LiberationBase):
    pass


class LiberationUpdate(LiberationBase):
    pass


class LiberationRead(LiberationBase, ReadNamedModel):

    class Config:
        orm_mode = True
