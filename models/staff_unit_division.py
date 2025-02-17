from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models import Model


class StaffUnitDivisions(Model):
    __tablename__ = 'hr_erp_staff_unit_divisions'
    
    staff_unit_id = Column(String(36), ForeignKey('hr_erp_staff_units.id'))
    curator_of_id = Column(String(36), ForeignKey('hr_erp_staff_divisions.id'))
    
    # relationships
    staff_unit = relationship("StaffUnit", back_populates="curators")
    staff_division = relationship("StaffDivision", back_populates="curators")