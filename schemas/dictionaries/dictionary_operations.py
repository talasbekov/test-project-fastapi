from typing import List
from schemas import CustomBaseModel


class JoinRecordsBody(CustomBaseModel):
    correct_id: str
    ids_to_change: List[str]
