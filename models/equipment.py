import uuid

from sqlalchemy import BigInteger, Column, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import TimeBaseModel

from .association import hr_document_equipments


class Equipment(TimeBaseModel, Base):

    __tablename__ = "equipments"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(150), nullable=True)
    quantity = Column(BigInteger, nullable=True)
    hr_documents = relationship("HrDocument", secondary=hr_document_equipments,
                                back_populates="equipments")
