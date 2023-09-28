from sqlalchemy import Column, Integer

from models import NamedModel


class FamilyRelation(NamedModel):
    family_order = Column(Integer)
    __tablename__ = "hr_erp_family_relations"
