from sqlalchemy import Column, ForeignKey, TEXT, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Survey(NamedModel):

    __tablename__ = "surveys"

    description = Column(TEXT, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("survey_types.id"))
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    type = relationship("SurveyType", foreign_keys=[type_id], back_populates="surveys")
    questions = relationship("Question", cascade="all,delete", back_populates="survey")
