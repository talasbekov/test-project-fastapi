from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class Properties(Model):

    __tablename__ = "properties"

    type_id = Column(UUID(as_uuid=True), ForeignKey("property_types.id"))

    purchase_date = Column(TIMESTAMP(timezone=True), nullable=False)
    purchase_type = Column(String(255), nullable=True)
    purchase_typeKZ = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    profile_id = Column(UUID(as_uuid=True),
                        ForeignKey("additional_profiles.id"))
    profile = relationship("AdditionalProfile", back_populates="properties")

    type = relationship("PropertyType", back_populates="properties")
