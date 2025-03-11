from typing import List
from schemas import Model


class JoinRecordsBody(Model):
    correct_id: str
    ids_to_change: List[str]
