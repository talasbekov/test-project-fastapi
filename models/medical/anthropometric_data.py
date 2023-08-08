from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models import Model


class AnthropometricData(Model):

    __tablename__ = "hr_erp_anthropometric_data"

    head_circumference = Column(Integer)
    shoe_size = Column(Integer)
    neck_circumference = Column(Integer)
    shape_size = Column(Integer)
    bust_size = Column(Integer)

    profile_id = Column(String(), ForeignKey("hr_erp_medical_profiles.id"))

    profile = relationship("MedicalProfile")
