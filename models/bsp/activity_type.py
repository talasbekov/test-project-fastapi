from sqlalchemy import Column, ForeignKey, TEXT, String, Boolean
from sqlalchemy.orm import relationship


from models import NamedModel

class ActivityType(NamedModel):
    __tablename__ = 'hr_erp_activity_types'

    # Relationships
    activities = relationship("Activity", back_populates="activity_type")

