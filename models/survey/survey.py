import enum

from sqlalchemy import Column, ForeignKey, TEXT, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel

    
class Survey(NamedModel):

    __tablename__ = "surveys"

    description = Column(TEXT, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    is_anonymous = Column(Boolean(), default=False, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    questions = relationship("Question", cascade="all, delete", back_populates="survey")
