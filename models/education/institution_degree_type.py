from sqlalchemy.orm import relationship

from models import NamedModel


class InstitutionDegreeType(NamedModel):

    __tablename__ = "institution_degree_types"

    education = relationship("Education", back_populates="degree")
