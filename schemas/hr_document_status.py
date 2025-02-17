from schemas import NamedModel, ReadNamedModel


class HrDocumentStatusBase(NamedModel):
    pass


class HrDocumentStatusCreate(HrDocumentStatusBase):
    pass


class HrDocumentStatusUpdate(HrDocumentStatusBase):
    pass


class HrDocumentStatusRead(HrDocumentStatusBase, ReadNamedModel):

    class Config:
        orm_mode = True
