from sqlalchemy import func
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from exceptions import ForbiddenException
from models import (StaffUnit,
                    PositionNameEnum, StaffDivisionEnum,
                    StatusEnum, CandidateStatusEnum, User,
                    StaffDivision, UserLoggingActivity)
from services import (staff_division_service, staff_unit_service,
                      position_service, hr_vacancy_service,
                      candidate_stage_type_service, candidate_service,
                      candidate_stage_info_service, status_service,)

class DashboardService:

    ALL_STATE_VIEWERS = [
        PositionNameEnum.POLITICS_GOVERNMENT_SERVANT.value,
        PositionNameEnum.HEAD_OF_DEPARTMENT.value,
        PositionNameEnum.MANAGEMENT_HEAD.value,
        PositionNameEnum.HEAD_OF_OTDEL.value
    ]

    def get_all_state(self, db: Session, role: str) -> int:

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(
            db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return self.__retrieve_all_staff_unit_count(db, staff_division)
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return self.__retrieve_all_staff_unit_count(db, staff_division)

    def get_state_by_list(self, db: Session, role: str) -> int:
        all_state = self.get_all_state(db, role)
        hr_vacancy = self.get_hr_vacancy_count_by_division \
            (db, role)
        state_by_list = all_state - len(hr_vacancy)
        return state_by_list

    def get_hr_vacancy_count_by_division(self, db: Session, 
    role: str) -> int:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(
            db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return hr_vacancy_service.get_vacancies_recursive(db, staff_division)
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return hr_vacancy_service\
                .get_vacancies_recursive(db, staff_division)

    def get_in_line_count_by_status(self, db: Session, role: str):

        state_by_list = self.get_state_by_list(db, role)
        state_by_status = self.get_count_by_status_all_users(db, role)
        state_in_line = state_by_list - len(state_by_status)

        return state_in_line

    def get_count_by_status_all_users(self, db: Session, role: str):

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return status_service.get_count_all_users_recursive_by_status(
                        db, staff_division
                    )
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )

            return status_service.get_count_all_users_recursive_by_status(
                        db, staff_division
                    )

    def get_count_by_every_status_users(
            self, db: Session, role: str
    ) -> dict[str, int]:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return {
                'ezhegodnyi_otpusk': status_service.get_users_recursive_by_status(
                        db, staff_division, StatusEnum.ANNUAL_LEAVE.value
                    ),
                'Otpusk_po_raportu': status_service.get_users_recursive_by_status(
                        db, staff_division, StatusEnum.VACATION.value
                    ),
                'v_komandirovke': status_service.get_users_recursive_by_status(
                        db, staff_division, StatusEnum.BUSINESS_TRIP.value
                    ),
                'na_bolnichnom': status_service.get_users_recursive_by_status(
                        db, staff_division, StatusEnum.SICK_LEAVE.value
                    ),
            }

        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )

            return {
                'ezhegodnyi_otpusk': status_service.get_users_recursive_by_status(
                    db, staff_division, StatusEnum.ANNUAL_LEAVE.value
                ),
                'Otpusk_po_raportu': status_service.get_users_recursive_by_status(
                    db, staff_division, StatusEnum.VACATION.value
                ),
                'v_komandirovke': status_service.get_users_recursive_by_status(
                    db, staff_division, StatusEnum.BUSINESS_TRIP.value
                ),
                'na_bolnichnom': status_service.get_users_recursive_by_status(
                    db, staff_division, StatusEnum.SICK_LEAVE.value
                ),
            }

    def get_all_active_candidates(
            self, db: Session, role: str
    ) -> int:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return candidate_service.get_candidates_recursive(
                db, staff_division
            )
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return candidate_service.get_candidates_recursive(
                db, staff_division
            )

    def get_statistic_passed_candidate_stage_infos(self, db: Session, role: str):
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            candidates = candidate_service.get_all(db)
        else:
            candidates = (
                candidate_service.get_all_by_staff_division(db,
                                                            staff_unit.staff_division,
                                                            CandidateStatusEnum.ACTIVE.value)
            )

        count_candidate_stages = candidate_stage_type_service.get_count(db)

        less_than_25 = 0
        between_25_50 = 0
        between_50_75 = 0
        more_than_75 = 0

        for candidate in candidates:
            passed_stages = (
                candidate_stage_info_service.get_count_passed_stages(db,
                                                                     candidate.id)
            )

            if passed_stages < count_candidate_stages / 4:
                less_than_25 += 1
            elif passed_stages < count_candidate_stages / 2:
                between_25_50 += 1
            elif passed_stages < count_candidate_stages * 3 / 4:
                between_50_75 += 1
            else:
                more_than_75 += 1

        return {
            'less_than_25': less_than_25,
            'between_25_50': between_25_50,
            'between_50_75': between_50_75,
            'more_than_75': more_than_75
        }

    def get_statistic_duration_candidate_learning(self, db: Session, role: str):
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            candidates = candidate_service.get_all(db)
        else:
            candidates = (
                candidate_service.get_all_by_staff_division(db,
                                                            staff_unit.staff_division,
                                                            CandidateStatusEnum.ACTIVE.value)
            )

        less_than_3_month = 0
        between_3_6_month = 0
        between_6_12_month = 0
        more_than_year = 0

        date_now = datetime.now(timezone.utc)

        for candidate in candidates:
            # Check if the candidate has been learning for more than a year
            if date_now - candidate.created_at > timedelta(days=365):
                more_than_year += 1
            # Check if the candidate has been learning for between 6-12 months
            elif date_now - candidate.created_at > timedelta(days=180):
                between_6_12_month += 1
            # Check if the candidate has been learning for between 3-6 months
            elif date_now - candidate.created_at > timedelta(days=90):
                between_3_6_month += 1
            # Check if the candidate has been learning for less than 3 months
            else:
                less_than_3_month += 1

        return {
            'less_than_3_month': less_than_3_month,
            'between_3_6_month': between_3_6_month,
            'between_6_12_month': between_6_12_month,
            'more_than_year': more_than_year
        }

    def get_statistic_completed_candidates(self, db: Session):
        completed_candidates_count = (
            candidate_service.get_count_completed_candidates(db)
        )

        return {
            'last_week': completed_candidates_count,
            'last_month': completed_candidates_count,
            'last_year': completed_candidates_count,
        }

    def get_curators_by_candidates(
            self, db: Session, role: str
    ) -> dict[str, int]:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return candidate_service.get_top_curators_by_candidates(
                db, staff_division
            )
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return candidate_service.get_top_curators_by_candidates(
                db, staff_division
            )

    def get_curators_by_candidates_duration(
            self, db: Session, role: str
    ) -> dict[str, int]:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.curator_of_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return candidate_service.get_top_curator_duration_by_candidates(
                db, staff_division
            )
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return candidate_service.get_top_curator_duration_by_candidates(
                db, staff_division
            )

    def get_all_users_of_erp(self, db: Session) -> int:
        users = db.query(User).count()
        return users

    def get_all_new_users_at_week(self, db: Session) -> int:
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=168)
        users = db.query(User).filter(
            User.created_at.between(start_date, end_date)
        ).count()
        return users

    def get_active_users(self, db: Session) -> int:
        active_users = db.query(User).filter(
            User.is_active == 1
        ).count()
        return active_users

    def get_users_at_three_day_by_active(self, db: Session):
        three_days_ago = datetime.now() - timedelta(hours=72)

        # Создаём подзапрос, который выбирает активных пользователей и группирует их по департаментам
        active_users_subquery = db.query(
            StaffDivision.name,
            func.count().label("active_users")
        ).join(
            StaffUnit, StaffUnit.staff_division_id == StaffDivision.id
        ).join(
            User, User.staff_unit_id == StaffUnit.id
        ).join(
            UserLoggingActivity
        ).filter(
            User.last_signed_at >= three_days_ago
        ).group_by(StaffDivision.name).subquery()

        # Создаём запрос, который выбирает общее количество пользователей по департаментам
        total_users_subquery = db.query(
            StaffDivision.name,
            func.count().label("total_users")
        ).join(
            StaffUnit, StaffUnit.staff_division_id == StaffDivision.id
        ).join(
            User, User.staff_unit_id == StaffUnit.id
        ).group_by(
            StaffDivision.name
        ).subquery()

        # Объединяем оба подзапроса и выполните запрос
        result = db.query(
            total_users_subquery.c.name,
            total_users_subquery.c.total_users,
            active_users_subquery.c.active_users
        ).outerjoin(active_users_subquery, total_users_subquery.c.name == active_users_subquery.c.name).all()

        # Теперь у нас есть данные о пользователях, их активности и департаментах

        activity_data_by_department = {}

        for name, total_users, active_users in result:
            activity_data_by_department[name] = {
                "total_users": total_users,
                "active_users": active_users if active_users is not None else 0
            }

        return activity_data_by_department

    def check_by_role(self, db: Session, staff_unit) -> bool:
        """
            Checks if a user with the given role
            ID has permission to view number of all state of SGO RK.
        """
        available_all_roles = [position_service.get_id_by_name(
            db, name) for name in self.ALL_STATE_VIEWERS]

        return any(staff_unit.position_id == i for i in available_all_roles)

    def __retrieve_all_staff_unit_count(self, db: Session, staff_division):

        # Получаем все дочерние штатные группы пользователя, включая саму группу
        all_states_count = (
            db.query(func.count(StaffUnit.id)).filter(
            StaffUnit.staff_division_id == staff_division.id
            ).scalar()
        )
        # Recursively call this function
        # for each child division and collect the counts in a list
        for child in staff_division.children:
            all_states_count += self.__retrieve_all_staff_unit_count(db, child)

        return all_states_count


dashboard_service = DashboardService()
