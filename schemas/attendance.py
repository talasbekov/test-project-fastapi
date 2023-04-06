from sqlalchemy import TEXT, Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models import Model

class Attendance(Model):

    __tablename__ = "ranks"

    physical_training = Column(Integer, nullable=True, default=100)
    tactical_training = Column(Integer, nullable=True, default=100)
    shooting_training = Column(Integer, nullable=True, default=100)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="attendance")
