from sqlalchemy import Column, ForeignKey, Table

from core import Base


hr_document_equipments = Table(
    "hr_erp_hr_document_equipments",
    Base.metadata,
    Column("document_id", ForeignKey("hr_erp_hr_documents.id")),
    Column("subject_id", ForeignKey("hr_erp_equipments.id")),
)

hr_documents_users = Table(
    "hr_erp_hr_document_users",
    Base.metadata,
    Column("document_id", ForeignKey("hr_erp_hr_documents.id")),
    Column("subject_id", ForeignKey("hr_erp_users.id"))
)

staff_unit_function = Table(
    "hr_erp_staff_unit_functions",
    Base.metadata,
    Column(
        "staff_unit_id",
        ForeignKey(
            "hr_erp_staff_units.id",
            ondelete="CASCADE",
            onupdate="CASCADE"),
        primary_key=True),
    Column(
        "staff_function_id",
        ForeignKey(
            "hr_erp_staff_functions.id",
            ondelete="CASCADE",
            onupdate="CASCADE"),
        primary_key=True)
)

u_liber_liberations = Table(
    "hr_erp_u_liber_liberations",
    Base.metadata,
    Column("user_liberation_id", ForeignKey("hr_erp_user_liberations.id")),
    Column("liberation_id", ForeignKey("hr_erp_liberations.id"))
)

s_u_cand_stage_infos = Table(
    "hr_erp_s_u_cand_stage_infos",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("hr_erp_staff_units.id")),
    Column("candidate_stage_info_id", ForeignKey("hr_erp_candidate_stage_infos.id"))
)

hr_v_hr_vacancy_req = Table(
    "hr_erp_hr_v_hr_vacancy_req",
    Base.metadata,
    Column("hr_vacancy_id", ForeignKey("hr_erp_hr_vacancies.id")),
    Column("hr_vacancy_requirement_id",
           ForeignKey("hr_erp_hr_vac_req.id"))
)

family_violation = Table(
    "hr_erp_family_violations",
    Base.metadata,
    Column("family_id", ForeignKey("hr_erp_families.id")),
    Column("violation_id", ForeignKey("hr_erp_violations.id"))
)

family_abroad_travel = Table(
    "hr_erp_family_abroad_travels",
    Base.metadata,
    Column("family_id", ForeignKey("hr_erp_families.id"), primary_key=True),
    Column("abroad_travel_id", ForeignKey("hr_erp_abroad_travels.id"), primary_key=True)
)

answers_options = Table(
    "hr_erp_answers_options",
    Base.metadata,
    Column("option_id", ForeignKey("hr_erp_options.id")),
    Column("answer_id", ForeignKey("hr_erp_answers.id"))
)
