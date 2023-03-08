from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Language(Model, Base):

    __tablename__ = "languages"

    name = Column(String)

    language_proficiency = relationship("LanguageProficiency")
