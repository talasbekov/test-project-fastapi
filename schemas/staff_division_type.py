from schemas import NamedModel, ReadNamedModel


class StaffDivisionTypeBase(NamedModel):
    pass


class StaffDivisionTypeCreate(StaffDivisionTypeBase):
    pass


class StaffDivisionTypeUpdate(StaffDivisionTypeBase):
    pass


class StaffDivisionTypeRead(StaffDivisionTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True
