from typing import Optional, Any, List
from schemas import Model, NamedModel, ReadModel, ReadNamedModel, CustomBaseModel


class CoolnessTypeBase(NamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessTypeCreate(CoolnessTypeBase):
    order: Optional[int]
#    percentage: Optional[int]


class CoolnessTypeUpdate(CoolnessTypeBase):
    pass


class CoolnessTypeRead(CoolnessTypeBase, ReadNamedModel):
    pass


class CoolnessTypeReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[CoolnessTypeRead]]


class CoolnessBase(Model):
    coolness_status: Optional[Any]
    type_id: Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    # @root_validator(pre=True)
    # def fill_none_values(cls, values):
    #     # Превращаем GetterDict в обычный dict, чтобы можно было делать item assignment
    #     values = dict(values)
    #     """
    #     Если поле None, заменяем его "жёстким" значением:
    #      - coolness_status → "Данные отсутствуют!"
    #      - type_id → "missing_type_id"
    #      - user_id → "missing_user"
    #     """
    #     values["coolness_status"] = values.get("coolness_status") or "Данные отсутствуют!"
    #     values["type_id"] = values.get("type_id") or str(uuid.uuid4())
    #     values["user_id"] = values.get("user_id") or str(uuid.uuid4())
    #
    #     return values


class CoolnessCreate(CoolnessBase):
    pass


class CoolnessUpdate(CoolnessBase):
    pass


class CoolnessRead(CoolnessBase, ReadModel):
    type: Optional[CoolnessTypeRead]

