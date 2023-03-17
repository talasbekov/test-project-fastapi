from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class HrDocumentStatus(NamedModel, Base):

    __tablename__ = "hr_document_statuses"
