from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from models import NamedModel


class City(NamedModel):

    __tablename__ = "hr_erp_cities"
    is_village = Column(Boolean, default=False, nullable=False)
    region_id = Column(String, ForeignKey("hr_erp_regions.id"), nullable=True)

    region = relationship("Region", back_populates="cities")
    birthplace = relationship("Birthplace", back_populates="city")