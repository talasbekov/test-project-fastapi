import datetime
import uuid
from typing import Optional

from schemas import Model, NamedModel


class StatRead(NamedModel):
    score: int
    abb: str

class HexagonBase(Model):
    KP: StatRead
    LS: StatRead
    EC: StatRead
    PZ: StatRead
    OP: StatRead
    FP: StatRead

class HexagonRead(HexagonBase):
    id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    
class HexagonAveragesRead(Model):
    KP: int
    LS: int
    EC: int
    PZ: int
    OP: int
    FP: int