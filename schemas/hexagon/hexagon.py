# import datetime
# import random
#
# from pydantic import Field
# from typing import Optional
#
# from schemas import Model, NamedModel
#
#
# class StatRead(NamedModel):
#     score: float = Field(default_factory=random.uniform(1.01, 5.00))
#     # abb: Optional[str]
#
#
# class HexagonBase(Model):
#     KP: StatRead
#     LS: StatRead
#     EC: StatRead
#     PZ: StatRead
#     OP: StatRead
#     FP: StatRead
#
#
# class HexagonRead(HexagonBase):
#     # id: Optional[str]
#     created_at: Optional[datetime.datetime]
#     updated_at: Optional[datetime.datetime]
#
#
# class HexagonAveragesRead(Model):
#     KP: float
#     LS: float
#     EC: float
#     PZ: float
#     OP: float
#     FP: float
