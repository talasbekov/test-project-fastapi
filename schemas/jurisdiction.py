from schemas import NamedModel, ReadNamedModel


class JurisdictionBase(NamedModel):
    pass


class JurisdictionCreate(JurisdictionBase):
    pass


class JurisdictionUpdate(JurisdictionBase):
    pass


class JurisdictionRead(JurisdictionBase, ReadNamedModel):

    class Config:
        orm_mode = True
