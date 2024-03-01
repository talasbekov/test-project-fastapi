from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class UserFinancialInfo(Model):

    __tablename__ = "hr_erp_user_financial_infos"

    iban = Column(String)
    housing_payments_iban = Column(String)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    profile = relationship(
        "PersonalProfile",
        back_populates="user_financial_infos")
