from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class Properties(Model):

    __tablename__ = "hr_erp_properties"

    type_id = Column(String(), ForeignKey("hr_erp_property_types.id"))

    purchase_date = Column(TIMESTAMP(timezone=True), nullable=False)
    purchase_type = Column(String(255), nullable=True)
    purchase_typeKZ = Column('purchase_typekz', String(255), nullable=True)
    address = Column(String(255), nullable=False)
    profile_id = Column(String(),
                        ForeignKey("hr_erp_additional_profiles.id"))
    profile = relationship("AdditionalProfile", back_populates="properties")

    type = relationship("PropertyType", back_populates="properties")
