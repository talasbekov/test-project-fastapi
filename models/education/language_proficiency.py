from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import NamedModel


class LanguageProficiency(NamedModel):

    __tablename__ = "language_proficiencies"

    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=True)
    language = relationship("Language", back_populates="language_proficiency")

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="language_proficiency")
