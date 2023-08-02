from enum import IntEnum

from sqlalchemy import Column, ForeignKey, Integer, Enum, TIMESTAMP, String
from sqlalchemy.orm import relationship

from models import Model


class PlanStatus(IntEnum):
    ACTIVE = 1
    DRAFT = 2


class BspPlan(Model):
    __tablename__ = 'bsp_plans'

    year = Column(Integer)
    creator_id = Column(String(), ForeignKey('users.id'))
    status = Column(Enum(PlanStatus))
    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    creator = relationship('User')
    schedule_years = relationship('ScheduleYear', back_populates='plan'
                                  , cascade='all,delete')
