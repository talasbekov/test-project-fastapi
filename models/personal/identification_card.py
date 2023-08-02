from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class IdentificationCard(Model):

    __tablename__ = "identification_cards"

    document_number = Column(String)
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    issued_by = Column(String)
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("personal_profiles.id"),
        nullable=False)

    profile = relationship(
        "PersonalProfile",
        back_populates="identification_card")
