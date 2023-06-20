import uuid

from sqlalchemy.orm import Session

from models import Attestation
from schemas import AttestationCreate, AttestationUpdate
from .base import ServiceBase


class AttestationService(
        ServiceBase[Attestation, AttestationCreate, AttestationUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, value):
        pass
