from sqlalchemy import Column, TEXT, ForeignKey, String
from sqlalchemy.orm import relationship
import enum

from models import Model

class SenderTypeEnum(str, enum.Enum):
    SURVEY = "Опрос"
    HR_DOCUMENT = "Приказ"
    BSP = "БСП"

class Notification(Model):
    __tablename__ = "hr_erp_notifications"

    message = Column(TEXT, nullable=False)

    sender_type = Column(
        String(),
        nullable=False,)
    receiver_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=False,
        index=True)

    receiver = relationship("User", foreign_keys=[receiver_id])
