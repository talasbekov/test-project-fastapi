from sqlalchemy.orm import relationship

from models import NamedModel


class Language(NamedModel):

    __tablename__ = "hr_erp_languages"

    language_proficiency = relationship(
        "LanguageProficiency",
        back_populates="language")
