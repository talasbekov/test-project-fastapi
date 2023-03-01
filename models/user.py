import uuid
from typing import Any

from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import Mapped, relationship

from core import Base
from models import Model

from .association import hr_documents_users, users_badges


class User(Model, Base):

    __tablename__ = "users"

    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    father_name = Column(String(150), nullable=True)
    icon = Column(TEXT(), nullable=True)
    call_sign = Column(String(255), unique=True)
    id_number = Column(String(255), unique=True)
    phone_number = Column(String(32))
    address = Column(String(255))
    rank_id = Column(
        UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)
    
    status = Column(String(255), nullable=True)
    status_till = Column(TIMESTAMP(timezone=True), nullable=True)

    birthday = Column(Date, nullable=True)
    description = Column(TEXT, nullable=True)

    rank = relationship("Rank", cascade="all,delete")
    badges = relationship(
        "Badge",
        secondary=users_badges,
        back_populates='users',
        cascade="all,delete"
    )

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_documents_users,
        back_populates="users",
        cascade="all,delete"
    )
