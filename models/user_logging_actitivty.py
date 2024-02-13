import uuid

from sqlalchemy import Column, ForeignKey, TIMESTAMP, text, String
from sqlalchemy.orm import relationship

from core import Base


"""
    UserActivity model for tracking user logging in
    
"""
class UserLoggingActivity(Base):
    
    
    def __init__(self, user_id: str):
        
        self.user_id = user_id
    
    
    __tablename__ = 'hr_erp_user_logging_activities'
    
    id = Column(String(), primary_key=True,
            nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    signed_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="activities")
