import uuid

from sqlalchemy import Column, BigInteger, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from core import Base
from .association import hr_document_equipments


class Equipment(Base):

    __tablename__ = "equipments"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(150), nullable=True)
    quantity = Column(BigInteger, nullable=True)
    hr_documents = relationship("Equipment", secondary="hr_document_equipments",
                                back_populates="hr_documents")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
