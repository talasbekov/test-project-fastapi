from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import Model


class BiographicInfo(Model):

    __tablename__ = "hr_erp_biographic_infos"
    gender = Column(Boolean)
    address = Column(String)
    family_status_id = Column(
        String(),
        ForeignKey("hr_erp_family_statuses.id"))
    residence_address = Column(String)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)
    personal_profile_id = Column(String(), nullable=True)
    # user_id = Column(String(), ForeignKey("hr_erp_users.id"), nullable=True)
    
    citizenship_id = Column(String(), ForeignKey("hr_erp_citizenships.id"),nullable=True)
    nationality_id = Column(String(), ForeignKey("hr_erp_nationalities.id"),nullable=True)
    birthplace_id = Column(String(), ForeignKey("hr_erp_birthplaces.id"),nullable=True)

    birthplace = relationship("Birthplace", back_populates="biographic_info")
    citizenship = relationship("Citizenship", back_populates="biographic_info")
    nationality = relationship("Nationality", back_populates="biographic_info")
    # user = relationship("User", back_populates="biographic_info")
    family_status = relationship("FamilyStatus", back_populates="biographic_info")
    profile = relationship("PersonalProfile", back_populates="biographic_info")
