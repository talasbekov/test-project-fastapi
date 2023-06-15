from schemas import NamedModel, ReadNamedModel


class CountryBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase, ReadNamedModel):
    pass
