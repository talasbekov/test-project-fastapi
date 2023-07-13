from sqlalchemy import Column, ForeignKey, Date, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from .association import (
    exam_schedule_instructors,
)


class ExamResult(Model):
    __tablename__ = "exam_results"

    # Properties
    exam_date = Column(Date)
    grade = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    exam_id = Column(UUID(as_uuid=True), ForeignKey('exam_schedules.id'))

    # Relationships
    user = relationship("User", back_populates="exam_results")
    exam = relationship("ExamSchedule")



class ExamSchedule(Model):
    __tablename__ = "exam_schedules"

    # Properties
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    place_id = Column(UUID(as_uuid=True), ForeignKey("places.id"))
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedule_years.id"))

    # Relationships
    instructors = relationship("User", secondary=exam_schedule_instructors)
    place = relationship("Place")
    schedule = relationship("ScheduleYear", back_populates="exams")
