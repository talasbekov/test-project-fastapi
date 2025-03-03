import uuid
from typing import Optional, List

from schemas import Model, ReadModel, HrDocumentRead, SurveyRead, UserShortRead


class NotificationBase(Model):
    message: str
    sender_type: str
    receiver_id: str
    sender_id: Optional[str] = "system"

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class NotificationRead(ReadModel, NotificationBase):
    message: Optional[str]
    sender_type: Optional[str]
    receiver_id: Optional[str]
    sender_id: Optional[str] = "system"
 
class NotificationReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[NotificationRead]]

class DetailedNotificationBase(Model):
    hr_document_id: Optional[str]
    receiver_id: Optional[str]
    survey_id: Optional[str]
    
class DetailedNotificationCreate(DetailedNotificationBase):
    pass

class DetailedNotificationUpdate(DetailedNotificationBase):
    pass

class SurveyNotificationRead(SurveyRead):
    owner: Optional[UserShortRead]
    owner_id: Optional[str]

class DetailedNotificationRead(ReadModel, DetailedNotificationBase):
    hr_document: Optional[HrDocumentRead]
    survey: Optional[SurveyNotificationRead]
    
class DetailedNotificationReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[DetailedNotificationRead]]
    