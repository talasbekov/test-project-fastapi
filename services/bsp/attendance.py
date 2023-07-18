import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Attendance, AttendedUser
from schemas import AttendanceCreate, AttendanceUpdate
from services.base import ServiceBase


class AttendanceService(ServiceBase[Attendance, AttendanceCreate, AttendanceUpdate]):
    def get_percentage_by_user_id(self, db: Session, user_id: uuid.UUID):
        attendances_count = (db.query(func.count('id'), Attendance.schedule_id)
                            .join(Attendance.attended_users)
                            .filter(AttendedUser.user_id == user_id)
                            .group_by(Attendance.schedule_id)
                            .all()
                            )
        
        return attendances_count
        # attended_count = (db.query(Attendance)
        #                   .join(Attendance.attended_users)
        #                   .filter(AttendedUser.user_id == user_id)
        #                   .filter(AttendedUser.is_attended == True)
        #                   .group_by(Attendance.schedule_id)
        #                   .count(Attendance.id)
        #                   .all()
        #                   )


attendance_service = AttendanceService(Attendance)
