from sqlalchemy import Column, String
from core import Base


class SocketSession(Base):
    __tablename__ = "hr_erp_socket_sessions"

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
    
    user_id = Column(
        String(),
        primary_key=True,
        nullable=False,
        index=True)
