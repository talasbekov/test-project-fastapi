from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Family(Model):

    __tablename__ = "families"

    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    IIN = Column(String)
    relation = Column(String)
    birthday = Column(TIMESTAMP(timezone=True), nullable=False)
    death_day = Column(TIMESTAMP(timezone=True))
    birthplace = Column(String)
    address = Column(String)
    workplace = Column(String)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("family_profiles.id"))

    profile = relationship("FamilyProfile", back_populates="family")
