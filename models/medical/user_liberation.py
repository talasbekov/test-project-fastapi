from sqlalchemy import Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.types import PickleType

from models import Model
from models.association import u_liber_liberations


class UserLiberation(Model):

    __tablename__ = "hr_erp_user_liberations"

    reason = Column(String)
    reasonKZ = Column("REASONKZ", String)
    initiator = Column(String)
    initiatorKZ = Column("INITIATORKZ", String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(String(), ForeignKey("hr_erp_medical_profiles.id"))
    liberation_ids = Column(PickleType, default=[])

    profile = relationship("MedicalProfile")
