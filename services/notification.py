from sqlalchemy.orm import Session

from models import Notification
from schemas import NotificationCreate, NotificationUpdate
from .base import ServiceBase

class NotificationService(ServiceBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_received_by_user_id(self, db: Session, user_id: str, skip: int = 0, limit: int = 10):
        return (
            db.query(self.model)
            .filter(self.model.receiver_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


notification_service = NotificationService(Notification)
