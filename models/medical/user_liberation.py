from sqlalchemy import Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model
from models.association import u_liber_liberations


class UserLiberation(Model):

    __tablename__ = "hr_erp_user_liberations"

    reason = Column(String)
    initiator = Column(String)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(String(), ForeignKey("hr_erp_medical_profiles.id"))
    liberation_id = Column(String(), ForeignKey("hr_erp_liberations.id"))

    profile = relationship("MedicalProfile")
    liberations = relationship(
        "Liberation",
        secondary=u_liber_liberations,
        back_populates='user_liberations',
        cascade="all,delete"
    )
