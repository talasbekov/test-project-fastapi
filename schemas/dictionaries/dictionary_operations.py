from typing import List
from pydantic import BaseModel


class JoinRecordsBody(BaseModel):
    correct_id: str
    ids_to_change: List[str]
