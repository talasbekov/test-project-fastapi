from sqlalchemy import Column, TEXT, ForeignKey, String, Boolean
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

    receiver_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=False,
        index=True)

    is_seen = Column(
        Boolean,
        nullable=False,
        default=False)
    
    type = Column(
        String(),
        nullable=True,
        default="Приказ")
    
    arbitrary_id = Column(
        String(),
        nullable=True)
    
    receiver = relationship("User", foreign_keys=[receiver_id])
