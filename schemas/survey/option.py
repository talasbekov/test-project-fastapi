import uuid

from typing import Optional, List

from schemas import Model, ReadModel

# base
class OptionBase(Model):
    question_id: uuid.UUID
    text: Optional[str]
    

class OptionMultipleChoiceBase(OptionBase):
    answers: List[uuid.UUID]


class OptionScaleBase(OptionBase):
    min_value: int
    max_value: int


class OptionGridBase(OptionBase):
    row_position: int
    column_position: int


class OptionCheckboxGridBase(OptionBase):
    row_position: int
    column_position: int
    is_checked: bool
    

# create
class OptionCreate(OptionBase):
    pass


class OptionMultipleChoiceCreate(OptionMultipleChoiceBase):
    pass


class OptionScaleCreate(OptionScaleBase):
    pass


class OptionGridCreate(OptionGridBase):
    pass


class OptionCheckboxGridCreate(OptionCheckboxGridBase):
    pass
    

# update
class OptionUpdate(OptionBase):
    pass


class OptionMultipleChoiceUpdate(OptionMultipleChoiceBase):
    answers: List[uuid.UUID]


class OptionScaleUpdate(OptionScaleBase):
    min_value: Optional[int]
    max_value: Optional[int]


class OptionGridUpdate(OptionGridBase):
    row_position: Optional[int]
    column_position: Optional[int]


class OptionCheckboxGridUpdate(OptionCheckboxGridBase):
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]


# read
class OptionRead(OptionBase, ReadModel):
    pass

    class Config:
        orm_mode = True


class OptionMultipleChoiceRead(OptionMultipleChoiceBase, ReadModel):
    answers: Optional[List[uuid.UUID]]
    
    class Config:
        orm_mode = True


class OptionScaleRead(OptionScaleBase, ReadModel):
    min_value: Optional[int]
    max_value: Optional[int]
    
    class Config:
        orm_mode = True


class OptionGridRead(OptionGridBase, ReadModel):
    row_position: Optional[int]
    column_position: Optional[int]
    
    class Config:
        orm_mode = True


class OptionCheckboxGridRead(OptionCheckboxGridBase, ReadModel):
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]
    
    class Config:
        orm_mode = True
