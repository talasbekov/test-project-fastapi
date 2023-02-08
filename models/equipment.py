import uuid

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class Equipment(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(150), nullable=True),
    quantity = Column(BigInteger, nullable=True),
    hr_documents = relationship("Equipment", secondary="hr_document_equipment",
                                back_populates="hr_documents")
