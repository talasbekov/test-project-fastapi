import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class DispensaryRegistration(Model):

    __tablename__ = "dispensary_registrations"

    