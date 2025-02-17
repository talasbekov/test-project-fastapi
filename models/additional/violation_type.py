from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import NamedModel

class ViolationType(NamedModel):
    __tablename__ = "hr_erp_violation_types"

    violations = relationship("Violation", back_populates="violation_type")