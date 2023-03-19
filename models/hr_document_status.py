from core import Base
from models import NamedModel


class HrDocumentStatus(NamedModel, Base):

    __tablename__ = "hr_document_statuses"
