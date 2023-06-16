from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class Attestation(Model):

    __tablename__ = "attestations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="attestations")
    attestation_history = relationship(
        "AttestationHistory",
        back_populates="attestation",
        cascade="all, delete-orphan",
        uselist=False)
