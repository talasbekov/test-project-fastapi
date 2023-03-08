from sqlalchemy import Column, String

from core import Base
from models import Model


class Institution(Model, Base):

    __tablename__ = "institutions"

    name = Column(String)
