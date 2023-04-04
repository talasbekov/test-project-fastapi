from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import Model
# model which contains may be name, or last_name, or father_name


class NameChange(Model):
    __tablename__ = "name_changes"

    name_before = Column(String, nullable=True)
    name_after = Column(String, nullable=True)

    last_name_before = Column(String, nullable=True)
    last_name_after = Column(String, nullable=True)

    father_name_before = Column(String, nullable=True)
    father_name_after = Column(String, nullable=True)
 
