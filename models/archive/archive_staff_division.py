import json

from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import NamedNestedModel


class ArchiveStaffDivision(NamedNestedModel):

    __tablename__ = "hr_erp_archive_staff_divisions"

    # Properties
    parent_group_id = Column(String(), ForeignKey(
        "hr_erp_archive_staff_divisions.id"), nullable=True)
    description = Column(CLOB)
    is_combat_unit = Column(Boolean)
    leader_id = Column(String(), ForeignKey(
        "hr_erp_archive_staff_units.id"), nullable=True)
    staff_division_number = Column(Integer)
    type_id = Column(String(), ForeignKey(
        "hr_erp_staff_division_types.id"), nullable=True)
    type = relationship("StaffDivisionType")
    staff_list_id = Column(
        String(),
        ForeignKey("hr_erp_staff_lists.id"),
        nullable=False)
    origin_id = Column(
        String(),
        ForeignKey("hr_erp_staff_divisions.id"),
        nullable=True)

    # Relationships
    children = relationship(
        "ArchiveStaffDivision",
        foreign_keys="ArchiveStaffDivision.parent_group_id",
        cascade="all, delete",
        lazy="joined")
    staff_list = relationship('StaffList',
                              back_populates='archive_staff_divisions')
    staff_units = relationship(
        "ArchiveStaffUnit",
        foreign_keys="ArchiveStaffUnit.staff_division_id",
        cascade="all, delete")
    leader = relationship(
        "ArchiveStaffUnit",
        cascade="all, delete",
        foreign_keys=leader_id,
        post_update=True)

@listens_for(ArchiveStaffDivision, 'before_update')
def description_set_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)
        
@listens_for(ArchiveStaffDivision, 'before_insert')
def description_set_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)