from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import NamedModel


class InstitutionDegreeType(NamedModel):

    __tablename__ = "institution_degree_types"

    education = relationship("Education", back_populates="degree")
