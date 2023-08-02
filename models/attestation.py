from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class Attestation(Model):

    __tablename__ = "attestations"

    user_id = Column(String(), ForeignKey("users.id"))
    user = relationship("User", back_populates="attestations")
    attestation_history = relationship(
        "AttestationHistory",
        back_populates="attestation",
        cascade="all, delete-orphan",
        uselist=False)
