from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import Model

class Birthplace(Model):
    __tablename__ = "hr_erp_birthplaces"

    name = Column(String, nullable=True, default='Unknown')
    country_id = Column(String, ForeignKey("hr_erp_countries.id"))
    region_id = Column(String, ForeignKey("hr_erp_regions.id"), nullable=True)
    city_id = Column(String, ForeignKey("hr_erp_cities.id"), nullable=True)

    country = relationship("Country", back_populates="birthplace")
    region = relationship("Region", back_populates="birthplace")
    city = relationship("City", back_populates="birthplace")
    biographic_info = relationship("BiographicInfo", back_populates="birthplace")
    family = relationship("Family", back_populates="birthplace")