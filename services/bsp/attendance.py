import uuid

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from models import Attendance, AttendedUser, AttendanceStatus
from schemas import (AttendanceCreate,
                     AttendanceUpdate,
                     AttendedUserCreate,
                     AttendancePercentageRead,)
from services.base import ServiceBase
from .schedule_year import schedule_year_service
from .attended_user import attended_user_service


class AttendanceService(ServiceBase[Attendance, AttendanceCreate, AttendanceUpdate]):

    def create(self, db: Session, attendance: AttendanceCreate):
        attendance = super().create(db, attendance)
        month_id = attendance.schedule_id
        schedule_year = schedule_year_service.get_by_schedule_month_id(db, month_id)
        users = schedule_year.users
        attended_users = []
        for user in users:
            attended_user_create = AttendedUserCreate(
                attendance_status=AttendanceStatus.ABSENT,
                attendance_id=attendance.id,
                user_id=user.id
                )
            attended_users.append(
                attended_user_service.create(db, attended_user_create))
        attendance.attended_users = attended_users

        db.add(attendance)
        db.flush()

        return attendance

    def get_percentage_by_user_id(self, db: Session, user_id: uuid.UUID):
        attendances_count = (db.query(func.count('id'), Attendance.schedule_id)
                             .join(Attendance.attended_users)
                             .filter(AttendedUser.user_id == user_id)
                             .group_by(Attendance.schedule_id)
                             .all()
                             )
        attendances_count_dict = {str(schedule_id): count
                                  for count, schedule_id
                                  in attendances_count}

        attended_count = (db.query(func.count('id'), Attendance.schedule_id)
                          .join(Attendance.attended_users)
                          .filter(AttendedUser.user_id == user_id)
                          .filter(or_(AttendedUser.attendance_status
                                      == AttendanceStatus.ATTENDED,
                                      AttendedUser.attendance_status
                                      == AttendanceStatus.ABSENT_REASON)
                                  )
                          .group_by(Attendance.schedule_id)
                          .all()
                          )
        attended_count_dict = {str(schedule_id): count
                               for count, schedule_id
                               in attended_count}
        attendances_percentages = []
        for key in attendances_count_dict.keys():
            year = schedule_year_service.get_by_schedule_month_id(db, key)
            try:
                percentage = ((attended_count_dict[key] * 100)
                              / attendances_count_dict[key])
            except KeyError:
                percentage = 0
            attendances_percentages.append(
                AttendancePercentageRead(activity=year.activity,
                                         percentage=percentage)
            )

        return attendances_percentages


attendance_service = AttendanceService(Attendance)
