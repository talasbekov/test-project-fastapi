from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

from models import NamedModel


class Region(NamedModel):

    __tablename__ = "hr_erp_regions"

    birthplace = relationship("Birthplace", back_populates="region")
    country_id = Column(String, ForeignKey('hr_erp_countries.id'),nullable=True)

    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region")