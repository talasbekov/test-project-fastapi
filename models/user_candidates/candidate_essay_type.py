from sqlalchemy.orm import relationship

from models import NamedModel


class CandidateEssayType(NamedModel):

    __tablename__ = "hr_erp_candidate_essay_types"

    candidate_essay_answers = relationship(
        "CandidateEssayAnswer",
        back_populates="candidate_essay_type")
