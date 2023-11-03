from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import Model


class HospitalData(Model):

    __tablename__ = "hr_erp_hospital_datas"

    code = Column(String)
    reason = Column(String)
    reasonKZ = Column("REASONKZ", String)
    place = Column(String)
    placeKZ = Column("PLACEKZ", String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(String(), ForeignKey("hr_erp_medical_profiles.id"))

    profile = relationship("MedicalProfile", back_populates="hospital_datas")
