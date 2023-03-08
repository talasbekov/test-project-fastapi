from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class TaxDeclaration(Model, Base):

    __tablename__ = "tax_declarations"

    year = Column(String)
    is_paid = Column(Boolean)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")
