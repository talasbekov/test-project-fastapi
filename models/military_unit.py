from sqlalchemy.orm import relationship

from models import NamedModel


class MilitaryUnit(NamedModel):

    __tablename__ = "hr_erp_military_units"

    user_oaths = relationship("UserOath", back_populates="military_unit")
