from sqlalchemy import Column, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import (
    schedule_month_instr,
)


class Place(NamedModel):
    __tablename__ = "hr_erp_places"


class ScheduleMonth(Model):
    __tablename__ = "hr_erp_schedule_months"

    # Properties
    start_date = Column(Date)
    end_date = Column(Date)
    place_id = Column(String(), ForeignKey("hr_erp_places.id"))
    schedule_id = Column(String(), ForeignKey("hr_erp_schedule_years.id"))

    # Relationships
    instructors = relationship("User", secondary=schedule_month_instr)
    place = relationship("Place")
    schedule = relationship("ScheduleYear", back_populates="months")
    days = relationship("ScheduleDay", back_populates="month"
                        , cascade='all,delete')
