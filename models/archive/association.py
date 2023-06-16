from sqlalchemy import Table, Column, ForeignKey
from core import Base

archive_staff_unit_function = Table(
    "archive_staff_unit_functions",
    Base.metadata,
    Column(
        "staff_unit_id",
        ForeignKey("archive_staff_units.id"),
        primary_key=True),
    Column(
        "staff_function_id",
        ForeignKey("archive_staff_functions.id"),
        primary_key=True)
)

archive_staff_unit_candidate_stage_infos = Table(
    "archive_staff_unit_candidate_stage_infos",
    Base.metadata,
    Column("archive_staff_unit_id", ForeignKey("archive_staff_units.id")),
    Column("candidate_stage_info_id", ForeignKey("candidate_stage_infos.id"))
)
