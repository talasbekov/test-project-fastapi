from sqlalchemy.orm import relationship

from models import NamedModel


class PropertyType(NamedModel):
    __tablename__ = "hr_erp_property_types"

    properties = relationship("Properties", back_populates="type")
    service_housings = relationship("ServiceHousing", back_populates="type")
