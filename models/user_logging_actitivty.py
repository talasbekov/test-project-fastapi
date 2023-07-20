import uuid

from sqlalchemy import Column, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base


"""
    UserActivity model for tracking user logging in
    
"""
class UserLoggingActivity(Base):
    
    
    def __init__(self, user_id: str):
        
        self.user_id = user_id
    
    
    __tablename__ = 'user_logging_activities'
    
    id = Column(UUID(as_uuid=True), primary_key=True,
            nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    signed_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="activities")
