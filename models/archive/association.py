from sqlalchemy import Table, Column, ForeignKey
from core import Base

archive_staff_unit_function = Table(
    "hr_erp_a_s_u_func",
    Base.metadata,
    Column(
        "staff_unit_id",
        ForeignKey("hr_erp_archive_staff_units.id"),
        primary_key=True),
    Column(
        "staff_function_id",
        ForeignKey("hr_erp_archive_staff_functions.id"),
        primary_key=True)
)

a_s_u_cand_stage_infos = Table(
    "hr_erp_a_s_u_cand_stage_infos",
    Base.metadata,
    Column("archive_staff_unit_id", ForeignKey("hr_erp_archive_staff_units.id")),
    Column("candidate_stage_info_id", ForeignKey("hr_erp_candidate_stage_infos.id"))
)
