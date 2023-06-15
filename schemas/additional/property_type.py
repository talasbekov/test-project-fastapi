from schemas import NamedModel, ReadNamedModel


class PropertyTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyTypeCreate(PropertyTypeBase):
    pass


class PropertyTypeUpdate(PropertyTypeBase):
    pass


class PropertyTypeRead(PropertyTypeBase, ReadNamedModel):
    pass
