from sqlalchemy import TEXT, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel


class Rank(NamedModel):

    __tablename__ = "hr_erp_ranks"

    rank_order = Column(Integer, nullable=True)
    military_url = Column(TEXT, nullable=True)
    employee_url = Column(TEXT, nullable=True)
    higher_rank_id = Column(String(), ForeignKey("hr_erp_ranks.id"), nullable=True)
    duration = Column(Integer, nullable=True)

    children = relationship('Rank')

