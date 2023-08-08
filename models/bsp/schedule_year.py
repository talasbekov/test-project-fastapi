from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import (
    schedule_year_s_d,
    schedule_year_months,
    schedule_exam_months,
    schedule_year_users,
)

class Month(NamedModel):
    order = Column(Integer)
    __tablename__ = 'hr_erp_months'


class ScheduleYear(Model):
    __tablename__ = 'hr_erp_schedule_years'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    # Properties
    plan_id = Column(String(), ForeignKey('hr_erp_bsp_plans.id'))
    activity_id = Column(String(), ForeignKey('hr_erp_activities.id'))
    is_exam_required = Column(Boolean)
    retry_count = Column(Integer)
    is_active = Column(Boolean)

    # Relationships
    staff_divisions = relationship(
        'StaffDivision',
        secondary=schedule_year_s_d)
    users = relationship(
        'User',
        secondary=schedule_year_users)
    activity = relationship('Activity')
    activity_months = relationship('Month', secondary=schedule_year_months)
    exam_months = relationship('Month', secondary=schedule_exam_months)
    plan = relationship('BspPlan', back_populates='schedule_years')
    months = relationship('ScheduleMonth', back_populates='schedule'
                          , cascade='all,delete')
    exams = relationship('ExamSchedule', back_populates='schedule'
                         , cascade='all,delete')
