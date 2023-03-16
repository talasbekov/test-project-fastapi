from core import Base

from models import NamedModel


class Jurisdiction(NamedModel, Base):

    __tablename__ = "jurisdictions"
