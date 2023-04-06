
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from enum import Enum as EnumBase


class PenaltyStatusEnum(EnumBase):
    reprimand = "Выговор"
    strict_reprimand = "Строгий выговор"
    warning = "Замечание"


class Penalty(Model):

    __tablename__ = "penalties"
    status = Column(Enum(PenaltyStatusEnum), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    