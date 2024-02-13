
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class PenaltyType(NamedModel):

    __tablename__ = "hr_erp_penalty_types"

    penalties = relationship("Penalty", back_populates="type")


class Penalty(Model):

    __tablename__ = "hr_erp_penalties"

    type_id = Column(String(), ForeignKey("hr_erp_penalty_types.id"))
    type = relationship("PenaltyType", back_populates="penalties")

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="penalties")
