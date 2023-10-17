from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import Model


class BiographicInfo(Model):

    __tablename__ = "hr_erp_biographic_infos"

    place_birth = Column(String)
    gender = Column(Boolean)
    citizenship = Column(String)
    nationality = Column(String)
    address = Column(String)
    family_status_id = Column(
        String(),
        ForeignKey("hr_erp_family_statuses.id"))
    residence_address = Column(String)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    family_status = relationship("FamilyStatus", cascade="all, delete")
    profile = relationship("PersonalProfile", back_populates="biographic_info")
