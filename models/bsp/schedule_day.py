from sqlalchemy import Column, ForeignKey, Time, Integer, String
from sqlalchemy.orm import relationship

from models import Model, NamedModel


class Day(NamedModel):
    __tablename__ = "hr_erp_days"
    order = Column(Integer)



class ScheduleDay(Model):
    __tablename__ = "hr_erp_schedule_days"

    # Properties
    day_id = Column(String(), ForeignKey("hr_erp_days.id"))
    start_time = Column(Time)
    end_time = Column(Time)
    month_id = Column(String(), ForeignKey("hr_erp_schedule_months.id"))

    # Relationships
    day = relationship("Day")
    month = relationship(
        "ScheduleMonth",
        back_populates="days",
    )
