from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from models import NamedModel


class StaffList(NamedModel):

    __tablename__ = "staff_lists"

    is_signed: bool = Column(Boolean, nullable=False, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    archive_staff_divisions = relationship("ArchiveStaffDivision", back_populates="staff_list")
    user = relationship("User", back_populates="staff_list", uselist=False)
