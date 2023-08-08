from sqlalchemy import Column, ForeignKey, Table

from core import Base


schedule_year_s_d = Table(
    "schedule_year_s_d",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("hr_erp_schedule_years.id")),
    Column("staff_division_id", ForeignKey("hr_erp_staff_divisions.id")),
)

schedule_year_users = Table(
    "schedule_year_users",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("hr_erp_schedule_years.id")),
    Column("user_id", ForeignKey("hr_erp_users.id")),
)

schedule_year_months = Table(
    "schedule_year_months",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("hr_erp_schedule_years.id")),
    Column("month_id", ForeignKey("hr_erp_months.id")),
)

schedule_exam_months = Table(
    "schedule_exam_months",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("hr_erp_schedule_years.id")),
    Column("month_id", ForeignKey("hr_erp_months.id")),
)

schedule_month_instr = Table(
    "schedule_month_instr",
    Base.metadata,
    Column("schedule_month_id", ForeignKey("hr_erp_schedule_months.id")),
    Column("user_id", ForeignKey("hr_erp_users.id")),
)

exam_schedule_inst = Table(
    "exam_schedule_inst",
    Base.metadata,
    Column("exam_schedule_id", ForeignKey("hr_erp_exam_schedules.id")),
    Column("user_id", ForeignKey("hr_erp_users.id")),
)
