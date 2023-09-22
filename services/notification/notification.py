from sqlalchemy.orm import Session

from models import Notification, SocketSession
from schemas import NotificationCreate, NotificationUpdate
from services import ServiceBase
from typing import TYPE_CHECKING

from ws import notification_manager

class NotificationService(
        ServiceBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_receiveds_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 10):
        notifications = (
            db.query(self.model)
            .filter(self.model.receiver_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        notifications_count = (db.query(self.model)
            .filter(self.model.receiver_id == user_id)
            .count())
        return {"total": notifications_count, "objects": notifications}
    
    async def send_message(
        self, message: str, user_id: str
    ):
        await notification_manager.broadcast(message, user_id)
        


notification_service = NotificationService(Notification)
