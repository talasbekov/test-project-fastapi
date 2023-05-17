from sqlalchemy import Column, ForeignKey, TEXT, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedNestedModel


class ArchiveStaffDivision(NamedNestedModel):

    __tablename__ = "archive_staff_divisions"

    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_divisions.id"), nullable=True)
    description = Column(TEXT)
    is_combat_unit = Column(Boolean)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_units.id"), nullable=True)

    description = Column(TEXT)
    children = relationship("ArchiveStaffDivision", foreign_keys=parent_group_id)

    staff_list_id = Column(UUID(as_uuid=True), ForeignKey("staff_lists.id"), nullable=False)
    staff_list = relationship('StaffList', back_populates='archive_staff_divisions')

    staff_units = relationship("ArchiveStaffUnit", back_populates="staff_division", foreign_keys="ArchiveStaffUnit.staff_division_id")

    origin_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    leader = relationship("ArchiveStaffUnit", foreign_keys=leader_id)
