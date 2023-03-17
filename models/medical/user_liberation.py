from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class UserLiberation(Model):

    __tablename__ = "user_liberations"

    reason = Column(String)
    liberation_name = Column(String)
    initiator = Column(String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    profile_id = Column(UUID(as_uuid=True), ForeignKey("medical_profiles.id"))

    profile = relationship("MedicalProfile")
