from sqlalchemy.orm import relationship

from models import NamedModel


class SportDegreeType(NamedModel):

    __tablename__ = "hr_erp_sport_degree_types"

    sport_degrees = relationship("SportDegree", back_populates="sport_degree_type")
