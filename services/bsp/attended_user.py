from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import AttendedUser, ScheduleMonth, Attendance, ScheduleYear, Activity
from schemas import (AttendedUserCreate,
                     AttendedUserUpdate,
                     AttendanceChangeStatus,
                     AttendanceChangeStatusWithSchedule,)
from services.base import ServiceBase



class AttendedUserService(ServiceBase[AttendedUser,
                                      AttendedUserCreate,
                                      AttendedUserUpdate]):
    def change_attendance_status(self, db: Session,
                                 body: AttendanceChangeStatus):
        attended_users = (
            db.query(AttendedUser)
            .filter(AttendedUser.attendance_id == body.attendance_id)
            .filter(AttendedUser.user_id.in_(body.user_ids))
            .update(
                {self.model.attendance_status: body.attendance_status,
                 self.model.reason: body.reason}
            )
        )

        return attended_users


    def change_attendance_status_by_schedule(self, db: Session,
                                             body: AttendanceChangeStatusWithSchedule):

        schedule_month_id = (
            db.query(ScheduleMonth.id)
            .join(ScheduleYear.months)
            .join(ScheduleYear.activity)
            .filter(ScheduleMonth.schedule_id == body.schedule_id)
            .filter(Activity.name == body.activity)
            .first()
        )
        attendance_id = (
            db.query(Attendance.id)
            .filter(Attendance.schedule_id == schedule_month_id)
            .filter(Attendance.attendance_date == body.date)
            .first()
        )
        if attendance_id is None:
            raise NotFoundException(
                detail=f"Attendance with id {id} not found!")
        user = (
            db.query(AttendedUser)
            .filter(AttendedUser.attendance_id == attendance_id)
            .filter(AttendedUser.user_id == body.user_id)
            .update(
                {self.model.attendance_status: body.attendance_status,
                 self.model.reason: body.reason}
            )
        )

        return user




attended_user_service = AttendedUserService(AttendedUser)
