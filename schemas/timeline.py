import uuid
from enum import Enum
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Any
from pydantic import BaseModel

from schemas import (
    Model,
    ReadModel,
    ReadNamedModel
)

time_zone = timezone(timedelta(hours=6))


class StatusEnum(Enum):
    granted = "Присвоен"
    confirmed = "Подтвержден"
    canceled = "Отменен"
    
    
class Event(Model):
    date: Optional[datetime]
    name: Optional[str]
    value: Optional[Any]
    type: Optional[str]
    

class TimeLineRead(Model):
    events: Optional[List[Event]]

    class Config:
        from_attributes=True
        arbitrary_types_allowed = True
