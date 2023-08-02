from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class UserFinancialInfo(Model):

    __tablename__ = "user_financial_infos"

    iban = Column(String)
    housing_payments_iban = Column(String)
    profile_id = Column(
        String(),
        ForeignKey("personal_profiles.id"),
        nullable=False)

    profile = relationship(
        "PersonalProfile",
        back_populates="user_financial_infos")
