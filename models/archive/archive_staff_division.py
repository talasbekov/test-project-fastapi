from sqlalchemy import Column, ForeignKey, Integer, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship
from core import Base
from models import NamedNestedModel


class ArchiveStaffDivision(NamedNestedModel, Base):

    __tablename__ = "archive_staff_divisions"

    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_divisions.id"), nullable=True)
    description = Column(TEXT)
    children = relationship("ArchiveStaffDivision", foreign_keys=parent_group_id)

    staff_list_id = Column(UUID(as_uuid=True), ForeignKey("staff_lists.id"), nullable=False)
    staff_list = relationship('StaffList', back_populates='archive_staff_divisions')

    staff_units = relationship("ArchiveStaffUnit", back_populates="staff_division")

    origin_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
