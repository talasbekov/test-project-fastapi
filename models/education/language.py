from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class Language(NamedModel):

    __tablename__ = "languages"

    language_proficiency = relationship("LanguageProficiency", back_populates="language")
