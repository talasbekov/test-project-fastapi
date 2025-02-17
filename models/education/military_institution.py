from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from models import NamedModel


class MilitaryInstitution(NamedModel):

    __tablename__ = "hr_erp_military_institutions"
    
    education = relationship("Education", back_populates="military_institution")
