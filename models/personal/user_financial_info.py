from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class UserFinancialInfo(Model, Base):

    __tablename__ = "user_financial_infos"

    iban = Column(String)
    housing_payments_iban = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")
