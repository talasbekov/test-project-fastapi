from sqlalchemy import Column, ForeignKey, TEXT, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from models import NamedNestedModel


class ArchiveStaffDivision(NamedNestedModel):

    __tablename__ = "archive_staff_divisions"

    # Properties
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_divisions.id"), nullable=True)
    description = Column(JSON(none_as_null=True))
    is_combat_unit = Column(Boolean)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_units.id"), nullable=True)

    staff_list_id = Column(UUID(as_uuid=True), ForeignKey("staff_lists.id"), nullable=False)
    origin_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    # Relationships
    children = relationship("ArchiveStaffDivision")
    staff_list = relationship('StaffList', back_populates='archive_staff_divisions')
    staff_units = relationship("ArchiveStaffUnit", back_populates="staff_division", foreign_keys="ArchiveStaffUnit.staff_division_id", cascade="all, delete")
    leader = relationship("ArchiveStaffUnit", foreign_keys=leader_id, post_update=True)
