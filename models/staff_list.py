from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class StaffList(NamedModel):

    __tablename__ = "staff_lists"

    status: str = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    user = relationship("User", back_populates="staff_list", uselist=False)
