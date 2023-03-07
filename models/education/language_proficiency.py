from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import Model


class LanguageProficiency(Model, Base):

    __tablename__ = "language_proficiencies"

    level = Column(Integer)

    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=True)
    language = relationship("Language")

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    profile = relationship("Profile")
