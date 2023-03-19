from sqlalchemy import TEXT, Column, Integer

from core import Base
from models import NamedModel


class Rank(NamedModel, Base):

    __tablename__ = "ranks"

    order = Column(Integer, nullable=True)
    military_url = Column(TEXT, nullable=True)
    employee_url = Column(TEXT, nullable=True)
