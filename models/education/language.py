from sqlalchemy.orm import relationship

from models import NamedModel


class Language(NamedModel):

    __tablename__ = "languages"

    language_proficiency = relationship(
        "LanguageProficiency",
        back_populates="language")
