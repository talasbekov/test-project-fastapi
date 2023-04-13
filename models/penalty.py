
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class PenaltyType(NamedModel):

    __tablename__ = "penalty_types"

    penalties = relationship("Penalty", back_populates="type")


class Penalty(NamedModel):

    __tablename__ = "penalties"

    type_id = Column(UUID(as_uuid=True), ForeignKey("penalty_types.id"))
    type = relationship("PenaltyType", back_populates="penalties")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="penalties")
