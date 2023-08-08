from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class ServiceHousing(Model):

    __tablename__ = "hr_erp_service_housings"

    type_id = Column(String(), ForeignKey("hr_erp_property_types.id"))
    address = Column(String(255))
    issue_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(String(255), nullable=False)

    profile_id = Column(String(),
                        ForeignKey("hr_erp_additional_profiles.id"))
    profile = relationship(
        "AdditionalProfile",
        back_populates="service_housing")

    type = relationship("PropertyType", back_populates="service_housings")
