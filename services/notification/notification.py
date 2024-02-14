import asyncio
import json

from sqlalchemy.orm import Session
from datetime import datetime
from models import Notification, SocketSession
from schemas import NotificationCreate, NotificationUpdate
from services import ServiceBase
from typing import Optional, Any, Dict, Union
from fastapi.encoders import jsonable_encoder

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
        self, db: Session, message: dict, user_id: str
    ):
        print(message)
        message["created_at"] = str(datetime.now())
        await notification_manager.broadcast(message, user_id)
        
    def notification_exists(self, db: Session, user_id: str, sender_type: str):
        return db.query(Notification).filter(
            Notification.receiver_id == user_id,
            Notification.type == sender_type
        ).first() is not None


notification_service = NotificationService(Notification)
