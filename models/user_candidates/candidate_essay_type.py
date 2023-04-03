from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel
 

class CandidateEssayType(NamedModel):

    __tablename__ = "candidate_essay_types"

    candidate_essay_answers = relationship("CandidateEssayAnswer", back_populates="candidate_essay_type")
