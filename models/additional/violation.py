from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import Model
from models.association import family_violation


class Violation(Model):

    __tablename__ = "hr_erp_violations"

    name = Column(String(255), nullable=False)
    nameKZ = Column('namekz', String, nullable=True)
    date = Column(
        'violation_date',
        TIMESTAMP(
            timezone=True),
        nullable=False,
        server_default=text("now()"))
    issued_by = Column(String(255), nullable=False)
    issued_byKZ = Column('issued_bykz', String, nullable=True)
    article_number = Column(String(255), nullable=False)
    article_numberKZ = Column('article_numberkz', String, nullable=True)
    consequence = Column(String(255), nullable=False)
    consequenceKZ = Column('consequencekz', String, nullable=True)
    document_link = Column(String(255), nullable=False)

    profile_id = Column(String(),
                        ForeignKey("hr_erp_additional_profiles.id"),
                        nullable=True)

    profile = relationship("AdditionalProfile", back_populates="violations")

    family_violation = relationship(
        "Violation",
        secondary=family_violation,
        cascade="all, delete")
