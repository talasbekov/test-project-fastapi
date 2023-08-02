from sqlalchemy import TEXT, Column, Integer

from models import NamedModel


class Rank(NamedModel):

    __tablename__ = "ranks"

    rank_order = Column(Integer, nullable=True)
    military_url = Column(TEXT, nullable=True)
    employee_url = Column(TEXT, nullable=True)
