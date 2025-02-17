from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import NamedModel

class Citizenship(NamedModel):
    __tablename__ = "hr_erp_citizenships"

    biographic_info = relationship("BiographicInfo", back_populates="citizenship")