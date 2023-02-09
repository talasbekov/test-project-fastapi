import uuid

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.orm import relationship

from core import Base
from .association import users_badges, hr_documents_users


class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    father_name = Column(String(150), nullable=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    call_sign = Column(String(255), unique=True)
    id_number = Column(String(255), unique=True)
    phone_number = Column(String(32))
    address = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
    actual_position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
    rank_id = Column(
        UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)

    birthday = Column(String, nullable=True)

    rank = relationship("Rank", cascade="all,delete")
    group = relationship("Group", cascade="all,delete", back_populates="users")
    badges = relationship(
        "Badge",
        secondary=users_badges,
        back_populates='users',
        cascade="all,delete"
    )
    position = relationship("Position", cascade="all,delete", foreign_keys=position_id)
    actual_position = relationship("Position", cascade="all,delete", foreign_keys=actual_position_id)

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_documents_users,
        back_populates="user",
        cascade="all,delete"
    )
