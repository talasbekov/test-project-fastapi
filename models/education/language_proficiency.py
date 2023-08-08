from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID, TEXT, DATE
from sqlalchemy.orm import relationship

from models import Model


class LanguageProficiency(Model):

    __tablename__ = "hr_erp_language_proficiencies"

    language_id = Column(
        String(),
        ForeignKey("hr_erp_languages.id"),
        nullable=True)
    language = relationship("Language", back_populates="language_proficiency")

    level = Column('language_level', Integer)

    profile_id = Column(String(), ForeignKey(
        "hr_erp_educational_profiles.id"), nullable=True)
    profile = relationship(
        "EducationalProfile",
        back_populates="language_proficiency")
    
    document_number = Column(String)
    document_link = Column(TEXT, nullable=True)
    assignment_date = Column(DATE)
