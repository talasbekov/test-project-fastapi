from sqlalchemy import Column, Integer

from models import Model


class AgeGroup(Model):

    __tablename__ = "age_groups"

    group = Column(Integer)

