import uuid
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from core import Base


class UserStat(Base):
    __tablename__ = "user_stats"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    physical_training = Column(Integer)
    fire_training = Column(Integer)
    attendance = Column(Integer)
    activity = Column(Integer)
    opinion_of_colleagues = Column(Integer)
    opinion_of_management = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
