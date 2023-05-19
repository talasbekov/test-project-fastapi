from sqlalchemy import Column, ForeignKey, Table

from core import Base


hr_document_equipments = Table(
    "hr_document_equipments",
    Base.metadata,
    Column("document_id", ForeignKey("hr_documents.id")),
    Column("subject_id", ForeignKey("equipments.id")),
)

hr_documents_users = Table(
    "hr_document_users",
    Base.metadata,
    Column("document_id", ForeignKey("hr_documents.id")),
    Column("subject_id", ForeignKey("users.id"))
)

staff_unit_function = Table(
    "staff_unit_functions",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("staff_units.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("staff_function_id", ForeignKey("staff_functions.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)

user_liberations_liberations = Table(
    "user_liberations_liberations",
    Base.metadata,
    Column("user_liberation_id", ForeignKey("user_liberations.id")),
    Column("liberation_id", ForeignKey("liberations.id"))
)

staff_unit_candidate_stage_infos = Table(
    "staff_unit_candidate_stage_infos",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("staff_units.id")),
    Column("candidate_stage_info_id", ForeignKey("candidate_stage_infos.id"))
)

hr_vacancy_hr_vacancy_requirements = Table(
    "hr_vacancy_hr_vacancy_requirements",
    Base.metadata,
    Column("vacancy_id", ForeignKey("hr_vacancies.id")),
    Column("requirement_id", ForeignKey("hr_vacancies_requirements.id"))
)
