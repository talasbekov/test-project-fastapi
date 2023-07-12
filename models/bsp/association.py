from sqlalchemy import Column, ForeignKey, Table

from core import Base


schedule_year_staff_divisions = Table(
    "schedule_year_staff_divisions",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("schedule_years.id")),
    Column("staff_division_id", ForeignKey("staff_divisions.id")),
)

schedule_year_users = Table(
    "schedule_year_users",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("schedule_years.id")),
    Column("user_id", ForeignKey("users.id")),
)

schedule_year_months = Table(
    "schedule_year_months",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("schedule_years.id")),
    Column("month_id", ForeignKey("months.id")),
)

schedule_exam_months = Table(
    "schedule_exam_months",
    Base.metadata,
    Column("schedule_year_id", ForeignKey("schedule_years.id")),
    Column("month_id", ForeignKey("months.id")),
)

schedule_month_instructors = Table(
    "schedule_month_instructors",
    Base.metadata,
    Column("schedule_month_id", ForeignKey("schedule_months.id")),
    Column("user_id", ForeignKey("users.id")),
)

exam_schedule_instructors = Table(
    "exam_schedule_instructors",
    Base.metadata,
    Column("exam_schedule_id", ForeignKey("exam_schedules.id")),
    Column("user_id", ForeignKey("users.id")),
)
