from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class HospitalData(Model):

    __tablename__ = "hospital_datas"

    code = Column(String)
    reason = Column(String)
    place = Column(String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(String(), ForeignKey("medical_profiles.id"))

    profile = relationship("MedicalProfile", back_populates="hospital_datas")
