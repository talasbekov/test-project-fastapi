from sqlalchemy import Column, ForeignKey, Time, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel


class Day(NamedModel):
    __tablename__ = "days"
    order = Column(Integer)



class ScheduleDay(Model):
    __tablename__ = "schedule_days"

    # Properties
    day_id = Column(UUID(as_uuid=True), ForeignKey("days.id"))
    start_time = Column(Time)
    end_time = Column(Time)
    month_id = Column(UUID(as_uuid=True), ForeignKey("schedule_months.id"))

    # Relationships
    day = relationship("Day")
    month = relationship(
        "ScheduleMonth",
        back_populates="days",
    )
