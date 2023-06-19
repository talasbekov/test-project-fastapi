import enum

from sqlalchemy import Column, ForeignKey, TEXT, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class SurveyTypeEnum(str, enum.Enum):
    REGULAR = "Обычный"
    ANONYMOUS = "Анонимный"
    

class Survey(NamedModel):

    __tablename__ = "surveys"

    description = Column(TEXT, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    type = Column(Enum(SurveyTypeEnum), nullable=False)
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    questions = relationship("Question", cascade="all,delete", back_populates="survey")
