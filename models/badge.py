from sqlalchemy import Column, String, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.oracle import NCLOB, CLOB
from models import Model, NamedModel


class BadgeType(NamedModel):
    __tablename__ = "hr_erp_badge_types"
    # name = Column(String, nullable=False)
    # nameKZ = Column('namekz', String, nullable=True)
    url = Column(NCLOB, nullable=True)
    badge_order = Column(Integer, nullable=True)

    badges = relationship("Badge", back_populates="type")


class Badge(Model):

    __tablename__ = "hr_erp_badges"

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    type_id = Column(String(), ForeignKey("hr_erp_badge_types.id"))
    type = relationship("BadgeType", back_populates="badges")
    user = relationship("User", back_populates='badges')

    history = relationship(
        "BadgeHistory",
        back_populates="badge",
        uselist=False)
