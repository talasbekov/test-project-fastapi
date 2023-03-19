from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class BiographicInfo(Model, Base):

    __tablename__ = "biographic_infos"

    place_birth = Column(String)
    date_birth = Column(TIMESTAMP(timezone=True))
    gender = Column(Boolean)
    citizenship = Column(String)
    nationality = Column(String)
    address = Column(String)
    family_status_id = Column(UUID(as_uuid=True), ForeignKey("family_statuses.id"))
    residence_address = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    family_status = relationship("FamilyStatus", cascade="all, delete")
    profile = relationship("PersonalProfile", back_populates="biographic_info")
