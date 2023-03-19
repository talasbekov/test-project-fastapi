from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class LanguageProficiency(Model):

    __tablename__ = "language_proficiencies"

    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=True)
    language = relationship("Language", back_populates="language_proficiency")

    level = Column(Integer)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="language_proficiency")
