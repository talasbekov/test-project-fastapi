from sqlalchemy import Column, ForeignKey, TEXT, String, Boolean
from sqlalchemy.orm import relationship


from models import Model


class Activity(Model):
    __tablename__ = 'hr_erp_activities'

    activity_type_id = Column(String(), ForeignKey(
        "hr_erp_activity_types.id"), nullable=True)
    # Properties  
    parent_group_id = Column(String(), ForeignKey(
        "hr_erp_activities.id"), nullable=True)
    instructions = Column(TEXT())
    is_time_required = Column(Boolean())
    normative_img = Column(TEXT(), nullable=True)
    # is_separated = Column(Boolean(), default=True)

    # Relationships
    children = relationship("Activity")
    activity_type = relationship("ActivityType", back_populates="activities")