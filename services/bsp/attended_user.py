from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException, BadRequestException
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
        if body.user_status is None:
            raise BadRequestException(
                detail=f"Got unexpected user_status {body}")
        for user_status in body.user_status:
            (
                db.query(AttendedUser)
                .filter(AttendedUser.attendance_id == body.attendance_id)
                .filter(AttendedUser.user_id == user_status.user_id)
                .update(
                    {AttendedUser.attendance_status: user_status.attendance_status,
                     AttendedUser.reason: user_status.reason}
                )
            )

        return None


    def change_attendance_status_by_schedule(self, db: Session,
                                             body: AttendanceChangeStatusWithSchedule):

        schedule_month = (
            db.query(ScheduleMonth)
            .join(ScheduleYear.months)
            .join(ScheduleYear.activity)
            .filter(ScheduleMonth.schedule_id == str(body.schedule_id))
            .filter(func.to_char(Activity.name) == body.activity)
            .first()
        )
        if schedule_month is None:
            raise NotFoundException(
                detail=f"ScheduleMonth with id {id} not found!")
        attendance = (
            db.query(Attendance)
            .filter(Attendance.schedule_id == str(schedule_month.id))
            .filter(Attendance.attendance_date == body.date)
            .first()
        )
        if attendance is None:
            raise NotFoundException(
                detail=f"Attendance with schedule_id {schedule_month.id} not found!")
        user = (
            db.query(AttendedUser)
            .filter(AttendedUser.attendance_id == str(attendance.id))
            .filter(AttendedUser.user_id == body.user_id)
            .update(
                {self.model.attendance_status: body.attendance_status,
                 self.model.reason: body.reason}
            )
        )

        return user




attended_user_service = AttendedUserService(AttendedUser)
