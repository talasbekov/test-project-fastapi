from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import Model


class UserStat(Model, Base):

    __tablename__ = "user_stats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    physical_training = Column(Integer)
    fire_training = Column(Integer)
    attendance = Column(Integer)
    activity = Column(Integer)
    opinion_of_colleagues = Column(Integer)
    opinion_of_management = Column(Integer)
