from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class DispensaryRegistration(NamedModel):

    __tablename__ = "dispensary_registrations"

    initiator = Column(String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("medical_profiles.id"))

    profile = relationship("MedicalProfile")
