from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class Violation(Model):

    __tablename__ = "violations"

    name = Column(String(255), nullable=False)
    date = Column(
        TIMESTAMP(
            timezone=True),
        nullable=False,
        server_default=text("now()"))
    issued_by = Column(String(255), nullable=False)
    article_number = Column(String(255), nullable=False)
    consequence = Column(String(255), nullable=False)

    profile_id = Column(UUID(as_uuid=True),
                        ForeignKey("additional_profiles.id"))

    profile = relationship("AdditionalProfile", back_populates="violations")
