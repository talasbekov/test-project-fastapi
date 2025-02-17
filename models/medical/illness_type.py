from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import NamedModel

class IllnessType(NamedModel):
    __tablename__ = "hr_erp_illness_types"

    hospital_datas = relationship("HospitalData", back_populates="illness_type")