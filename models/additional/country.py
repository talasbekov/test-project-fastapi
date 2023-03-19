from sqlalchemy.orm import relationship

from models import NamedModel


class Country(NamedModel):

    __tablename__ = "countries"

    abroad_travels = relationship("AbroadTravel", back_populates="destination_country")
