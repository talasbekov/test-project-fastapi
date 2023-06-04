from sqlalchemy import Column, ForeignKey, ARRAY, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from models import NamedModel
from .association import staff_unit_function, staff_unit_candidate_stage_infos


class StateBody(NamedModel):
    __tablename__ = "state_bodies"
