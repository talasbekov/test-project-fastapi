from sqlalchemy.orm import Session

from models import AttendedUser
from schemas import AttendedUserCreate, AttendedUserUpdate, AttendanceChangeStatus
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


attended_user_service = AttendedUserService(AttendedUser)
