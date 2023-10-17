from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import NamedModel


class DispensaryRegistration(NamedModel):

    __tablename__ = "hr_erp_disp_registrations"

    initiator = Column(String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(String(), ForeignKey("hr_erp_medical_profiles.id"))

    profile = relationship("MedicalProfile")
