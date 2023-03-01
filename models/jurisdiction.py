import uuid

from sqlalchemy import TIMESTAMP, Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import NamedModel


class Jurisdiction(NamedModel, Base):

    __tablename__ = "jurisdictions"
