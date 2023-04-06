
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from enum import Enum as EnumBase


class SpecialityEnum(EnumBase):
    speciality1 = "Специалист 1 класса - наставник (мастер)"
    speciality2 = "Специалист 2 класса - наставник (мастер)"
    speciality3 = "Специалист 3 класса - наставник (мастер)"


class Coolness(Model):

    __tablename__ = "coolnesses"
    speciality = Column(Enum(SpecialityEnum), nullable=True)
    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
