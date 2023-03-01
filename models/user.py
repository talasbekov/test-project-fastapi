import uuid
from typing import Any

from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import Mapped, relationship

from core import Base

from .association import hr_documents_users, user_permissions, users_badges, user_service_functions


class User(Base):

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
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
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
    service_functions = relationship(
        "ServiceFunction",
        secondary=user_service_functions,
        back_populates="users",
        cascade="all,delete"
    )
    staff_unit = relationship("StaffUnit", cascade="all,delete", foreign_keys=staff_unit_id)
    actual_staff_unit = relationship("StaffUnit", cascade="all,delete", foreign_keys=actual_staff_unit_id)

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_documents_users,
        back_populates="users",
        cascade="all,delete"
    )
