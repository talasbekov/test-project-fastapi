from sqlalchemy import Table, Column, ForeignKey
from core import Base

archive_staff_unit_function = Table(
    "archive_staff_unit_functions",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("archive_staff_units.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("staff_function_id", ForeignKey("archive_staff_functions.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)
