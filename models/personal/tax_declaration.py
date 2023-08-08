from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class TaxDeclaration(Model):

    __tablename__ = "hr_erp_tax_declarations"

    year = Column(String)
    is_paid = Column(Boolean)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    profile = relationship(
        "PersonalProfile",
        back_populates="tax_declarations")
