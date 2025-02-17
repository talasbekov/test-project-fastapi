import enum

from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from models import NamedModel


class StaffListStatusEnum(str, enum.Enum):
    APPROVED = "Утвержден"
    DIVERTED = "Отклонен"
    IN_PROGRESS = "В процессе"


class StaffList(NamedModel):

    __tablename__ = "hr_erp_staff_lists"

    is_signed: bool = Column(Boolean, nullable=False, default=False)
    user_id = Column(String(), ForeignKey("hr_erp_users.id"), nullable=True)
    document_signed_by = Column(String, nullable=True)
    document_signed_at = Column(TIMESTAMP(timezone=True),
                                nullable=True, server_default=text("now()"))
    rank = Column(String, nullable=True)
    document_number = Column(String, nullable=True)
    document_link = Column(String, nullable=True)
    status = Column(String, nullable=True)
    changes_size = Column(Integer, default=0, nullable=True)

    archive_staff_divisions = relationship(
        "ArchiveStaffDivision", back_populates="staff_list", cascade="all, delete")
    user = relationship("User", back_populates="staff_list", uselist=False)
