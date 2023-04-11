import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Attestation
from schemas import AttestationRead, AttestationCreate, AttestationUpdate
from .base import ServiceBase
from utils import is_valid_uuid


class AttestationService(ServiceBase[Attestation, AttestationCreate, AttestationUpdate]):
    
    def create_relation(self, db: Session, user_id: uuid.UUID, value):
        pass
