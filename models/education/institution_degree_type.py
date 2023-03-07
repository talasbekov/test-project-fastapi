from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import Model


class InstitutionDegreeType(Model, Base):

    __tablename__ = "institution_degree_types"

    name = Column(String)

    education_id = Column(UUID(as_uuid=True), ForeignKey("educations.id"), nullable=True)
    education = relationship("Education")
