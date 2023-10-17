import enum
from sqlalchemy import Column, ForeignKey, Date, String, Enum
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
    __tablename__ = "hr_erp_attended_users"

    # Properties
    attendance_status = Column(Enum(AttendanceStatus))
    reason = Column(String)
    user_id = Column(String(), ForeignKey('hr_erp_users.id'))
    attendance_id = Column(String(), ForeignKey('hr_erp_attendances.id',
                                                          ondelete="CASCADE"))
    # Relationships
    user = relationship("User")
    attendance = relationship("Attendance", back_populates="attended_users",)


class Attendance(Model):
    __tablename__ = "hr_erp_attendances"

    # Properties
    attendance_date = Column(Date)
    class_status = Column(Enum(ClassStatus))
    schedule_id = Column(String(), ForeignKey('hr_erp_schedule_months.id',
                                                        ondelete="CASCADE"))

    # Relationships
    schedule = relationship("ScheduleMonth", back_populates='attendances',
                            cascade='all,delete')
    attended_users = relationship("AttendedUser", back_populates="attendance",
                                  cascade='all,delete')
