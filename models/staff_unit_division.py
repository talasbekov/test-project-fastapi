from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models import Model


class StaffUnitDivision(Model):
    __tablename__ = 'HR_ERP_STAFF_UNIT_DIVISIONS'
    # Assuming your database is Oracle, you might need to specify the schema as well
    # __table_args__ = {'schema': 'SYSTEM'}
    
    STAFF_UNIT_ID = Column(String(36), ForeignKey('SYSTEM.HR_ERP_STAFF_UNITS.STAFF_UNIT_ID'), primary_key=True)
    CURATOR_OF_ID = Column(String(36), ForeignKey('SYSTEM.HR_ERP_STAFF_DIVISIONS.CURATOR_OF_ID'))
    
    # Define relationships
    staff_unit = relationship("StaffUnit", back_populates="staff_unit_divisions")
    staff_division = relationship("StaffDivision", back_populates="staff_unit_divisions")