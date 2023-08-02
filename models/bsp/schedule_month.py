from sqlalchemy import Column, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import (
    schedule_month_instructors,
)


class Place(NamedModel):
    __tablename__ = "places"


class ScheduleMonth(Model):
    __tablename__ = "schedule_months"

    # Properties
    start_date = Column(Date)
    end_date = Column(Date)
    place_id = Column(String(), ForeignKey("places.id"))
    schedule_id = Column(String(), ForeignKey("schedule_years.id"))

    # Relationships
    instructors = relationship("User", secondary=schedule_month_instructors)
    place = relationship("Place")
    schedule = relationship("ScheduleYear", back_populates="months")
    days = relationship("ScheduleDay", back_populates="month"
                        , cascade='all,delete')
