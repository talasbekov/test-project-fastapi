import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base

from .association import user_service_functions


class ServiceFunction(Base):

    __tablename__ = "service_functions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    service_function_type_id = Column(UUID(as_uuid=True), ForeignKey("service_function_types.id"), nullable=True)
    spend_hours_per_week = Column(Integer, nullable=True)

    service_function_type = relationship("ServiceFunctionType", cascade="all, delete")
    users = relationship(
        "User",
        secondary=user_service_functions,
        back_populates="service_functions",
        cascade="all,delete"
    )
