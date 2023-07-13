from sqlalchemy import Column, ForeignKey, Date, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class AttendedUser(Model):
    __tablename__ = "attended_users"

    # Properties
    is_attended = Column(Boolean)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    attendance_id = Column(UUID(as_uuid=True), ForeignKey('attendances.id'))
    # Relationships
    user = relationship("User")
    attendance = relationship("Attendance", back_populates="attended_users")


class AbsentUser(Model):
    __tablename__ = "absent_users"

    # Properties
    reason = Column(String)
    absent_date = Column(Date)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Relationships
    user = relationship("User")


class Attendance(Model):
    __tablename__ = "attendances"

    # Properties
    attendance_date = Column(Date)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey('schedule_months.id'))

    # Relationships
    schedule = relationship("ScheduleMonth")
    attended_users = relationship("AttendedUser", back_populates="attendance")
