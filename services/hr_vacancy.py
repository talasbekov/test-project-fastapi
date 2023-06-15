from typing import List
from sqlalchemy.orm import Session

from exceptions.client import BadRequestException, ForbiddenException, NotFoundException
from models import (HrVacancy, StaffUnit, StaffDivision,
                     PositionNameEnum, HrVacancyCandidate)
from models.hr_vacancy import HrVacancy
from schemas import (HrVacancyCreate, HrVacancyUpdate,
                     HrVacancyRead, HrVacancyStaffDivisionRead, HrVacancyUpdate,
                     HrVacancyCandidateRead)
from .base import ServiceBase
from .hr_vacancy_requirements import hr_vacancy_requirement_service
from .staff_unit import staff_unit_service
from .user import user_service
from .staff_division import staff_division_service
from .archive.archive_staff_unit import archive_staff_unit_service


class HrVacancyService(ServiceBase[HrVacancy, HrVacancyCreate, HrVacancyUpdate]):
    
    def get_multi(self, db: Session) -> List[HrVacancy]:
        
        vacancies = db.query(self.model).filter(
            self.model.is_active == True
        ).all()
        
        return vacancies
    
    
    def get_by_department(self, db: Session, staff_division_id: str):
    
        staff_division = staff_division_service.get_by_id(db, staff_division_id)
        vacancies = self._get_vacancies_recursive(db, staff_division)

        response = HrVacancyStaffDivisionRead(
            id = staff_division.id,
            name = staff_division.name,
            vacancies = [HrVacancyRead.from_orm(i).dict() for i in vacancies]
        )
        
        return response
    
    
    def get_multi_not_active(self, db: Session, skip: int = 0, limit: int = 100) -> List[HrVacancy]:
        vacancies = db.query(self.model).filter(
            self.model.is_active == False
        ).offset(skip).limit(limit).all()
        
        return vacancies


    def get_by_id(self, db: Session, id: str) -> HrVacancy:
        hr_vacancy = super().get(db, id)
        if hr_vacancy is None:
            raise NotFoundException(detail=f"HrVacancy with id: {id} is not found!")
        return hr_vacancy
    
    
    def get_by_archieve_staff_unit(self, db: Session, archieve_staff_unit_id: str) -> HrVacancy:
        hr_vacancy = db.query(self.model).filter(
            self.model.archive_staff_unit_id == archieve_staff_unit_id
        ).first()
        
        return hr_vacancy


    def create(self, db: Session, body: HrVacancyCreate, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        staff_unit = staff_unit_service.get_by_id(db, body.staff_unit_id)
        
        vacancy = self.model() # init object
        
        vacancy.staff_unit_id = staff_unit.id
        vacancy.is_active = body.is_active
        
        if body.hr_vacancy_requirements_ids is not None:
            vacancy.hr_vacancy_requirements = self._set_requirements_to_vacancy(db, body.hr_vacancy_requirements_ids)
        
        db.add(vacancy)
        db.flush()
        
        return vacancy
    
    
    def create_by_archive_staff_unit(self, db: Session, body: HrVacancyCreate, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        archieve_staff_unit = archive_staff_unit_service.get_by_id(db, body.staff_unit_id)
        
        vacancy = self.model() # init object
        
        vacancy.archive_staff_unit_id = archieve_staff_unit.id
        
        if body.hr_vacancy_requirements_ids is not None:
            vacancy.hr_vacancy_requirements = self._set_requirements_to_vacancy(db, body.hr_vacancy_requirements_ids)
        
        db.add(vacancy)
        db.flush()
        
        return vacancy
    
    
    def get_candidates(self, db: Session, id: str, role_id: str) -> List[HrVacancyCandidateRead]:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        vacancy = self.get_by_id(db, id)
        
        if vacancy.is_active is False:
            raise ForbiddenException(f"Vacancy with id {id} is not active!")
        
        return vacancy.candidates
    
    
    def respond_to_vacancy(self, db: Session, id: str, user_id: str):
        
        current_user = user_service.get_by_id(db, user_id)
        
        vacancy = self.get_by_id(db, id)
        
        if vacancy.is_active is False:
            raise ForbiddenException(f"Vacancy with id {id} is not active!")
        
        if self._check_exists_respond(db, id, user_id):
            raise BadRequestException(f"User with id {user_id} already responded to vacancy with id {id}!")
        
        hr_vacancy_candidate = HrVacancyCandidate(
            user_id=current_user.id,
            hr_vacancy_id=vacancy.id
        )
        
        db.add(hr_vacancy_candidate)
        db.flush()
        
        return vacancy


    def unactive(self, db: Session, id: str, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        vacancy = self.get_by_id(db, id)
        
        vacancy.is_active = False
        
        db.add(vacancy)
        db.flush()
        
        return vacancy
    
    
    def update(self, db: Session, id: str, body: HrVacancyUpdate, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        hr_vacancy = self.get_by_id(db, id)
        
        if body.hr_vacancy_requirements_ids is not None:
            hr_vacancy.hr_vacancy_requirements = self._set_requirements_to_vacancy(db, body.hr_vacancy_requirements_ids)
                
        if body.staff_unit_id is not None:
            hr_vacancy.staff_unit_id = staff_unit_service.get_by_id(db, body.staff_unit_id).id
            
        if body.is_active is not None:
            hr_vacancy.is_active = body.is_active
                        
        db.add(hr_vacancy)
        db.flush()
        
        return hr_vacancy
    
    
    def update_by_archieve_staff_unit(self, db: Session, id: str, body: HrVacancyUpdate, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        hr_vacancy = self.get_by_id(db, id)
        
        if body.hr_vacancy_requirements_ids is not None:
            hr_vacancy.hr_vacancy_requirements = self._set_requirements_to_vacancy(db, body.hr_vacancy_requirements_ids)
                
        if body.staff_unit_id is not None:
            hr_vacancy.staff_unit_id = archive_staff_unit_service.get_by_id(db, body.staff_unit_id).id
            
        if body.is_active is not None:
            hr_vacancy.is_active = body.is_active
                        
        db.add(hr_vacancy)
        db.flush()
        
        return hr_vacancy


    def _check_by_role(self, db: Session, role_id: str) -> bool:
        current_user_staff_unit = staff_unit_service.get_by_id(db, role_id)
        current_user_position = current_user_staff_unit.position
        
        if current_user_position.name != PositionNameEnum.HR:
            return False
        
        return True
    
    
    def _set_requirements_to_vacancy(self, db: Session, hr_vacancy_requirements_ids: List):
        vacancy_requirements = []
        
        for requirement in hr_vacancy_requirements_ids:
            requirement = hr_vacancy_requirement_service.get_by_id(db, requirement)
        
            vacancy_requirements.append(requirement)
        
        return vacancy_requirements
    
    
    def _get_vacancies_recursive(self, db: Session, department: StaffDivision):
        vacancies = db.query(self.model)\
            .join(StaffUnit, self.model.staff_unit_id == StaffUnit.id)\
            .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id)\
            .filter(
                self.model.is_active == True,
                self.model.staff_unit_id == StaffUnit.id,
                StaffUnit.staff_division_id == department.id
            ).all()
            
        # Recursively call this function for each child division
        for child in department.children:
            vacancies.extend(self._get_vacancies_recursive(db, child))
        
        return vacancies
    
    def _check_exists_respond(self, db: Session, id: str, user_id: str) -> bool:
        respond = (
            db.query(self.model)\
            .join(HrVacancyCandidate, HrVacancyCandidate.hr_vacancy_id == self.model.id)\
            .filter(
                HrVacancyCandidate.user_id == user_id,
                HrVacancyCandidate.hr_vacancy_id == id
            ).first()
        )
        
        return True if respond else False

hr_vacancy_service = HrVacancyService(HrVacancy)
