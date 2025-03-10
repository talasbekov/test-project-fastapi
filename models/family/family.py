from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
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
    address = Column(String)
    workplace = Column(String)
    document_link = Column(String, nullable=True)
    profile_id = Column(String, nullable=True)
    birthplace_id = Column(String(), ForeignKey("hr_erp_birthplaces.id"))
    birthplace_text = Column(String, nullable=True)

    relation_id = Column(String(), ForeignKey("hr_erp_family_relations.id"))
    families_profile_id = Column(String(), ForeignKey("hr_erp_family_profiles.id"))

    birthplace = relationship("Birthplace", back_populates="family")
    profile = relationship("FamilyProfile", back_populates="family")
    relation = relationship("FamilyRelation")
    violation = relationship(
        "Violation",
        secondary=family_violation,
        back_populates="families"  # связываем с атрибутом в Violation
    )
    abroad_travels = relationship(
        "AbroadTravel",
        secondary=family_abroad_travel,
        back_populates="families",
        cascade="all, delete"
    )
