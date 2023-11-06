from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum

from models import Model
from enum import Enum as EnumBase


class ReserveEnum(EnumBase):
    enlisted = "Зачислен"
    reserve = "Резерв"


class PersonalReserve(Model):

    __tablename__ = "hr_erp_personnal_reserves"
    reserve = Column(Enum(ReserveEnum), nullable=True)
    reserve_date = Column(TIMESTAMP(timezone=True), nullable=True)

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    document_link = Column(String, nullable=True)
    document_number = Column(String, nullable=True)
