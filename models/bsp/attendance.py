import enum
from sqlalchemy import Column, ForeignKey, Date, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class AttendanceStatus(str, enum.Enum):
    ATTENDED = 'Присутствует'
    LATE = 'Опоздал'
    ABSENT_REASON = 'Отсутствует(уважительная причина)'
    ABSENT = 'Отсутствует'

class ClassStatus(str, enum.Enum):
    STARTED = 'В процессе'
    COMPLETED = 'Завершен'
    WAITING = 'Ожидание'



class AttendedUser(Model):
    __tablename__ = "attended_users"

    # Properties
    attendance_status = Column(Enum(AttendanceStatus))
    reason = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    attendance_id = Column(UUID(as_uuid=True), ForeignKey('attendances.id'))
    # Relationships
    user = relationship("User")
    attendance = relationship("Attendance", back_populates="attended_users")


class Attendance(Model):
    __tablename__ = "attendances"

    # Properties
    attendance_date = Column(Date)
    class_status = Column(Enum(ClassStatus))
    schedule_id = Column(UUID(as_uuid=True), ForeignKey('schedule_months.id'))

    # Relationships
    schedule = relationship("ScheduleMonth")
    attended_users = relationship("AttendedUser", back_populates="attendance")
