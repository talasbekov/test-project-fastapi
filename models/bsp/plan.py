from enum import IntEnum

from sqlalchemy import Column, ForeignKey, Integer, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class PlanStatus(IntEnum):
    ACTIVE = 1
    DRAFT = 2


class BspPlan(Model):
    __tablename__ = 'bsp_plans'

    year = Column(Integer)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    status = Column(Enum(PlanStatus))
    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    creator = relationship('User')
    schedule_years = relationship('ScheduleYear', back_populates='plan')
