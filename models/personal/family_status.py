from core import Base

from models import NamedModel


class FamilyStatus(NamedModel, Base):

    __tablename__ = "family_statuses"
