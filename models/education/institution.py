from sqlalchemy.orm import relationship

from models import NamedModel


class Institution(NamedModel):

    __tablename__ = "hr_erp_institutions"

    education = relationship("Education", back_populates="institution")
