from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class Attestation(Model):

    __tablename__ = "hr_erp_attestations"

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="attestations")
    attestation_history = relationship(
        "AttestationHistory",
        back_populates="attestation",
        cascade="all, delete-orphan",
        uselist=False)
