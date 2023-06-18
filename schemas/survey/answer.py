import uuid

from typing import List, Optional, Dict

from schemas import Model, ReadModel

#Base
class AnswerBase(Model):
    question_id: uuid.UUID


class AnswerTextBase(AnswerBase):
    text: str
    

class AnswerSingleChoiceBase(AnswerBase):
    option_id: uuid.UUID
    

class AnswerMultipleChoiceBase(AnswerBase):
    options: List[uuid.UUID]
    

class AnswerScaleBase(AnswerBase):
    scale_value: int
    

class AnswerGridBase(AnswerBase):
    grid_values: Dict[str, Dict[str, bool]]
    

class AnswerCheckboxGridBase(AnswerBase):
    checkbox_grid_values: Dict[str, Dict[str, bool]]


#create
class AnswerTextCreate(AnswerTextBase):
    pass
    

class AnswerSingleChoiceCreate(AnswerSingleChoiceBase):
    pass
    

class AnswerMultipleChoiceCreate(AnswerMultipleChoiceBase):
    pass
    

class AnswerScaleCreate(AnswerScaleBase):
    pass
    

class AnswerGridCreate(AnswerGridBase):
    pass
    

class AnswerCheckboxGridCreate(AnswerCheckboxGridBase):
    pass


#update
class AnswerTextCreate(AnswerTextBase):
    pass
    

class AnswerSingleChoiceCreate(AnswerSingleChoiceBase):
    pass
    

class AnswerMultipleChoiceCreate(AnswerMultipleChoiceBase):
    pass
    

class AnswerScaleCreate(AnswerScaleBase):
    pass
    

class AnswerGridCreate(AnswerGridBase):
    pass
    

class AnswerCheckboxGridCreate(AnswerCheckboxGridBase):
    pass


# read
class AnswerTextRead(AnswerTextBase, ReadModel):
    question_id: Optional[uuid.UUID]
    text: Optional[str]
    
    class Config:
        orm_mode = True
    

class AnswerSingleChoiceRead(AnswerSingleChoiceBase, ReadModel):
    question_id: Optional[uuid.UUID]
    option_id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True
    

class AnswerMultipleChoiceRead(AnswerMultipleChoiceBase, ReadModel):
    question_id: Optional[uuid.UUID]
    options: Optional[List[uuid.UUID]]
    
    class Config:
        orm_mode = True


class AnswerScaleRead(AnswerScaleBase, ReadModel):
    question_id: Optional[uuid.UUID]
    scale_value: Optional[int]
    
    class Config:
        orm_mode = True
    

class AnswerGridRead(AnswerGridBase, ReadModel):
    question_id: Optional[uuid.UUID]
    grid_values: Optional[Dict[str, Dict[str, bool]]]
    
    class Config:
        orm_mode = True
    

class AnswerCheckboxGridRead(AnswerCheckboxGridBase, ReadModel):
    question_id: Optional[uuid.UUID]
    checkbox_grid_values: Optional[Dict[str, Dict[str, bool]]]
    
    class Config:
        orm_mode = True
