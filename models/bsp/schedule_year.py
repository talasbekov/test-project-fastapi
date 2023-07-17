from sqlalchemy import Column, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import (
    schedule_year_staff_divisions,
    schedule_year_months,
    schedule_exam_months,
    schedule_year_users,
)

class Month(NamedModel):
    __tablename__ = 'months'


class ScheduleYear(Model):
    __tablename__ = 'schedule_years'

    # Properties
    plan_id = Column(UUID(as_uuid=True), ForeignKey('bsp_plans.id'))
    activity_id = Column(UUID(as_uuid=True), ForeignKey('activities.id'))
    is_exam_required = Column(Boolean)
    retry_count = Column(Integer)

    # Relationships
    staff_divisions = relationship(
        'StaffDivision',
        secondary=schedule_year_staff_divisions)
    users = relationship(
        'User',
        secondary=schedule_year_users)
    activity = relationship('Activity')
    activity_months = relationship('Month', secondary=schedule_year_months)
    exam_months = relationship('Month', secondary=schedule_exam_months)
    plan = relationship('BspPlan', back_populates='schedule_years')
    months = relationship('ScheduleMonth', back_populates='schedule')
    exams = relationship('ExamSchedule', back_populates='schedule')
