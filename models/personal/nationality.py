from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import NamedModel

class Nationality(NamedModel):
    __tablename__ = "hr_erp_nationalities"

    biographic_info = relationship("BiographicInfo", back_populates="nationality")