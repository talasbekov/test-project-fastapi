from sqlalchemy import Column, TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class UserOath(Model):

    __tablename__ = "hr_erp_user_oaths"

    date = Column('oath_date', TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    military_unit = Column(String())

    # military_unit = relationship("MilitaryUnit", back_populates="user_oaths")
