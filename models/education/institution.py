from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from models import NamedModel


class Institution(NamedModel):

    __tablename__ = "hr_erp_institutions"

    education = relationship("Education", back_populates="institution")
    active = Column(Boolean, nullable=False, default=True)
