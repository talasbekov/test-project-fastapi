from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID

from models import Model
from enum import Enum as EnumBase


class ReserveEnum(EnumBase):
    enlisted = "Зачислен"
    reserve = "Резерв"


class PersonalReserve(Model):

    __tablename__ = "personnal_reserves"
    reserve = Column(Enum(ReserveEnum), nullable=True)
    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    document_link = Column(String, nullable=True)
    document_number = Column(String, nullable=True)
