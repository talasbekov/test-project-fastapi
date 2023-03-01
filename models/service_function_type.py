import uuid

from sqlalchemy import TEXT, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class ServiceFunctionType(Base):

    __tablename__ = "service_function_types"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
