from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..association import family_violation, family_abroad_travel

from models import Model


class Family(Model):

    __tablename__ = "hr_erp_families"

    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    IIN = Column(String)
    birthday = Column(TIMESTAMP(timezone=True), nullable=False)
    death_day = Column(TIMESTAMP(timezone=True))
    birthplace = Column(String)
    address = Column(String)
    workplace = Column(String)

    relation_id = Column(String(), ForeignKey("hr_erp_family_relations.id"))
    profile_id = Column(String(), ForeignKey("hr_erp_family_profiles.id"))

    profile = relationship("FamilyProfile", back_populates="family")
    relation = relationship("FamilyRelation")
    violation = relationship(
        "Violation",
        secondary=family_violation,
        cascade="all, delete")
    abroad_travel = relationship(
        "AbroadTravel",
        secondary=family_abroad_travel,
        cascade="all, delete")
