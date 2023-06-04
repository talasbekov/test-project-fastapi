from schemas import NamedModel, ReadNamedModel


class StateBodyBase(NamedModel):
    pass

class StateBodyCreate(StateBodyBase):
    pass

class StateBodyUpdate(StateBodyBase):
    pass

class StateBodyRead(StateBodyBase, ReadNamedModel):
    pass
