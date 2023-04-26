from sqlalchemy import Column, String, TEXT, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models import Model

class Notification(Model):
    __tablename__ = "notifications"

    message = Column(TEXT, nullable=False)

    sender_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
