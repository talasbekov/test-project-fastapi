import uuid

from sqlalchemy import BigInteger, Column, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model):

    __tablename__ = "profiles"
