from sqlalchemy import Column, ForeignKey, Time, Integer, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import activity_date_days


class Day(NamedModel):
    __tablename__ = "hr_erp_days"
    day_order = Column(Integer)


class ActivityDate(Model):
    __tablename__ = "hr_erp_activity_dates"
    activity_date = Column(Date)


class ScheduleDay(Model):
    __tablename__ = "hr_erp_schedule_days"

    # Properties
    day_id = Column(String(), ForeignKey("hr_erp_days.id"))
    start_time = Column(Time)
    end_time = Column(Time)
    month_id = Column(String(), ForeignKey("hr_erp_schedule_months.id"))
    activity_month_id = Column(String(),
                               ForeignKey("hr_erp_months.id"))

    # Relationships
    day = relationship("Day")
    month = relationship(
        "ScheduleMonth",
        back_populates="days",
    )
    activity_month = relationship("Month")
    activity_dates = relationship("ActivityDate",
                                  secondary=activity_date_days,
                                  cascade='all,delete')
