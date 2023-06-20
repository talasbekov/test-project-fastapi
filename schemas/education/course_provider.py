from schemas import NamedModel, ReadNamedModel


class CourseProviderBase(NamedModel):
    pass


class CourseProviderCreate(CourseProviderBase):
    pass


class CourseProviderUpdate(CourseProviderBase):
    pass


class CourseProviderRead(CourseProviderBase, ReadNamedModel):

    class Config:
        orm_mode = True
