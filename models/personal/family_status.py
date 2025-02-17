from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from models import NamedModel


class FamilyStatus(NamedModel):
    
    __tablename__ = "hr_erp_family_statuses"  

    #id = Column(String, primary_key=True)
    #name = Column(String, nullable=False)
    #nameKZ = Column(String, nullable=True)  
    #created_at = Column(DateTime)
    #updated_at = Column(DateTime)

    biographic_info = relationship("BiographicInfo", back_populates="family_status")
