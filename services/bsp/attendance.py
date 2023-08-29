import datetime
import uuid

from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session

from models import (Attendance,
                    AttendedUser,
                    AttendanceStatus,
                    ScheduleMonth,
                    ScheduleYear,
                    User,)
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
        users = schedule_year['objects'].users
        attended_users = []
        for user in users:
            attended_user_create = AttendedUserCreate(
                attendance_status=AttendanceStatus.ABSENT.name,
                attendance_id=attendance.id,
                user_id=user.id
                )
            attended_users.append(
                attended_user_service.create(db, attended_user_create))
        attendance.attended_users = attended_users

        db.add(attendance)
        db.flush()

        db.commit()
        return attendance

    def create_by_schedule_month(self, db: Session, schedule_month):
        for schedule_day in schedule_month.days:
            for weekday_date in schedule_day.activity_dates:
                params = {'attendance_date': str(weekday_date.activity_date),
                          'schedule_id': str(schedule_month.id),
                          'id': str(uuid.uuid4())}
                db.execute(text("""
                                INSERT INTO HR_ERP_ATTENDANCES
                                (attendance_date, schedule_id, id)
                                VALUES(TO_DATE(:attendance_date, 'YYYY-MM-DD'),
                                       :schedule_id,
                                       :id)
                                """),
                           params)


    def get_percentage_by_user_id(self, db: Session, user_id: str):
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
                          .filter(or_(func.to_char(AttendedUser.attendance_status)
                                      == AttendanceStatus.ATTENDED.name,
                                      func.to_char(AttendedUser.attendance_status)
                                      == AttendanceStatus.ABSENT_REASON.name)
                                  )
                          .group_by(Attendance.schedule_id)
                          .all()
                          )
        attended_count_dict = {str(schedule_id): count
                               for count, schedule_id
                               in attended_count}
        attendances_percentages = []
        for key in attendances_count_dict.keys():
            year = schedule_year_service.get_by_schedule_month_id(db, key)['objects']
            try:
                percentage = ((attended_count_dict[key] * 100)
                              / attendances_count_dict[key])
            except KeyError:
                percentage = 0
            if year is None:
                continue
            attendances_percentages.append(
                AttendancePercentageRead(activity=year.activity,
                                         percentage=percentage)
            )

        return attendances_percentages

    def get_absent_users(self, db: Session, schedule_id: str):
        schedule_months = (
            db.query(ScheduleMonth.id)
            .join(ScheduleYear.months)
            .filter(ScheduleMonth.schedule_id == schedule_id)
        )
        attendances = (
            db.query(Attendance.id)
            .filter(Attendance.schedule_id.in_(schedule_months))
        )

        absent_users = (
            db.query(User)
            .join(AttendedUser)
            .filter(AttendedUser.attendance_id.in_(attendances),
                    func.to_char(AttendedUser.attendance_status)
                    == AttendanceStatus.ABSENT_REASON.name)
            .all()
        )

        return absent_users

    def get_nearest_attendances(self, db: Session,
                                is_mine: bool,
                                user_id: uuid.UUID,
                                skip: int,
                                limit: int):
        current_date = datetime.date.today()

        attendances = (
            db.query(Attendance)
        )
        if is_mine:
            attendances = (attendances
                           .join(Attendance.attended_users)
                           .filter(AttendedUser.user_id == user_id)
                           )

        attendances = (attendances
                       .filter(Attendance.attendance_date >= current_date)
                       .order_by(Attendance.attendance_date.asc())
                       .offset(skip)
                       .limit(limit)
                       .all()
                       )

        total = (
            db.query(Attendance)
        )
        if is_mine:
            total = (total
                     .join(Attendance.attended_users)
                     .filter(AttendedUser.user_id == user_id)
                     )
        total = (total
                 .filter(Attendance.attendance_date >= current_date)
                 .order_by(Attendance.attendance_date.asc())
                 .offset(skip)
                 .limit(limit)
                 .count()
                 )

        return {"objects": attendances, "total": total}

    def get_attendance_users(self, db: Session, attendance_id: uuid.UUID):
        absent_users = (
            db.query(AttendedUser)
            .filter(AttendedUser.attendance_id == attendance_id)
            .all()
        )

        return absent_users


attendance_service = AttendanceService(Attendance)
