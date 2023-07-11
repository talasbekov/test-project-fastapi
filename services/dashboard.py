from typing import List

from sqlalchemy.orm import Session

from models import (StaffDivision, StaffUnit,
                    PositionNameEnum, StaffDivisionEnum,
                    StatusEnum, Status, User, StatusType)
from services import (staff_division_service, staff_unit_service,
                      position_service, hr_vacancy_service)


class DashboardService:
    ALL_STATE_VIEWERS = [
        PositionNameEnum.SUPERVISOR.value,
        PositionNameEnum.HEAD_OF_DEPARTMENT.value,
        PositionNameEnum.MANAGEMENT_HEAD.value,
        PositionNameEnum.HEAD_OF_OTDEL.value,
    ]

    ALL_STATUSES = [
        StatusEnum.ANNUAL_LEAVE.value,
        StatusEnum.VACATION.value,
        StatusEnum.BUSINESS_TRIP.value,
        StatusEnum.SICK_LEAVE.value,
        StatusEnum.MATERNITY_LEAVE.value
    ]

    def get_all_state(self, db: Session, role: str) -> int:

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.staff_division_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            return self.__retrieve_all_staff_unit_count(db, staff_division)
        elif not self.check_by_role(db, staff_unit):
            return 0
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            return self.__retrieve_all_staff_unit_count(db, staff_division)

    def get_state_by_list(self, db: Session, role: str) -> int:
        all_state = self.get_all_state(db, role)
        hr_vacancy = self.get_hr_vacancy_count_by_division\
            (db, role)
        state_by_list = all_state - hr_vacancy
        return state_by_list

    def get_hr_vacancy_count_by_division(self, db: Session,
                                         role: str) -> int:
        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)
        fifth_department = staff_division_service.get_by_name(db, "Пятый департамент")

        if staff_unit.staff_division_id == fifth_department.id:
            staff_division = staff_division_service.get_by_name(
                db, StaffDivisionEnum.SERVICE.value
            )
            print("5dep", hr_vacancy_service
                  .get_vacancies_recursive(db, staff_division))
            return len(hr_vacancy_service
                       .get_vacancies_recursive(db, staff_division))
        elif not self.check_by_role(db, staff_unit):
            print("true")
            return 0
        else:
            staff_division = staff_division_service.get_by_id(
                db, staff_unit.staff_division_id
            )
            print("false", len(hr_vacancy_service
                               .get_vacancies_recursive(db, staff_division)))
            return len(hr_vacancy_service
                       .get_vacancies_recursive(db, staff_division))

    def get_in_line_count_by_status(self, db: Session, role: str):

        # Получите пользователей с соответствующими статусами
        users = db.query(User).join(Status)\
            .join(StatusType).filter(
            StatusType.name.in_(self.ALL_STATUSES)
        ).all()
        users_with_status: List[User] = []
        for user in users:
            print(user.name)
            users_with_status.append(user.name)

        print([name for name in users_with_status])

        state_by_list = self.get_state_by_list(db, role)
        state_by_status = len([name for name in users_with_status])
        state_in_line = state_by_list - state_by_status
        print(state_in_line)
        return state_in_line

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
        staff_divisions: List[StaffDivision] = \
            staff_division_service.get_all_child_groups(
                db, staff_division.id)
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(
                staff_unit_service.get_by_staff_division_id(db, i.id))
        # print(len(staff_units))
        return len(staff_units)


dashboard_service = DashboardService()
