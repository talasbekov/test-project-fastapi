from sqlalchemy import Column, ForeignKey, Date, Integer, Time, Enum, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.oracle import CLOB

from models import Model
from .association import (
    exam_schedule_inst,
)
from .attendance import ClassStatus


class ExamResult(Model):
    __tablename__ = "hr_erp_exam_results"

    # Properties
    exam_date = Column(Date)
    grade = Column(Integer)
    results = Column(CLOB)
    is_active = Column(Boolean())
    user_id = Column(String(), ForeignKey('hr_erp_users.id'))
    exam_id = Column(String(), ForeignKey('hr_erp_exam_schedules.id'))

    # Relationships
    user = relationship("User", back_populates="exam_results")
    exam = relationship("ExamSchedule", back_populates="exam_results",
                        cascade='all,delete')



class ExamSchedule(Model):
    __tablename__ = "hr_erp_exam_schedules"

    # Properties
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    class_status = Column(Enum(ClassStatus))
    place_id = Column(String(), ForeignKey("hr_erp_places.id"))
    schedule_id = Column(String(), ForeignKey("hr_erp_schedule_years.id"))

    # Relationships
    instructors = relationship("User", secondary=exam_schedule_inst)
    place = relationship("Place")
    schedule = relationship("ScheduleYear", back_populates="exams")
    exam_results = relationship("ExamResult", back_populates="exam",
                                cascade='all,delete')
