import uuid
from typing import Any

from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import Mapped, relationship

from core import Base
from models import TimeBaseModel

from .association import (hr_documents_users, user_functions, user_permissions,
                          users_badges)


class User(TimeBaseModel, Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    father_name = Column(String(150), nullable=True)
    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    icon = Column(TEXT(), nullable=True)
    call_sign = Column(String(255), unique=True)
    id_number = Column(String(255), unique=True)
    phone_number = Column(String(32))
    address = Column(String(255))
    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    actual_staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    rank_id = Column(
        UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)
    
    status = Column(String(255), nullable=True)
    status_till = Column(TIMESTAMP(timezone=True), nullable=True)

    birthday = Column(Date, nullable=True)
    description = Column(TEXT, nullable=True)

    rank = relationship("Rank", cascade="all,delete")
    staff_division = relationship("StaffDivision", cascade="all,delete", back_populates="users")
    badges = relationship(
        "Badge",
        secondary=users_badges,
        back_populates='users',
        cascade="all,delete"
    )
    permissions = relationship(
        "Permission",
        secondary=user_permissions,
        back_populates="users",
        cascade="all,delete"
    )
    functions = relationship(
        "StaffFunction",
        secondary=user_functions,
        back_populates="users"
    )
    staff_unit = relationship("StaffUnit", cascade="all,delete", foreign_keys=staff_unit_id)
    actual_staff_unit = relationship("StaffUnit", cascade="all,delete", foreign_keys=actual_staff_unit_id)

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_documents_users,
        back_populates="users",
        cascade="all,delete"
    )
 