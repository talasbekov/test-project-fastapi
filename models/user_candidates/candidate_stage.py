from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
 

class CandidateStage(Model):

    __tablename__ = "candidate_stages"

    candidate = relationship("Candidate", back_populates="candidate_stage", uselist=False)
    candidate_stage_info = relationship("CandidateStageInfo", back_populates="candidate_stage", cascade="all, delete")
