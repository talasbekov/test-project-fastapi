from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions.client import ForbiddenException, NotFoundException
from models import HrVacancy, StaffUnit
from models.position import PositionNameEnum
from schemas import HrVacancyCreate, HrVacancyUpdate
from .base import ServiceBase
from .hr_vacancy_requirements import hr_vacancy_requirement_service
from .position import position_service
from .staff_unit import staff_unit_service
from .user import user_service
from .staff_division import staff_division_service


class HrVacancyService(ServiceBase[HrVacancy, HrVacancyCreate, HrVacancyUpdate]):
    
    def get_multi(self, db: Session) -> List[HrVacancy]:
        
        vacancies = db.query(self.model).filter(
            self.model.is_active == True
        ).all()
        
        return vacancies
    
    
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


    def create(self, db: Session, body: HrVacancyCreate, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        position = position_service.get_by_id(db, body.position_id)
        staff_division = staff_division_service.get_by_id(db, body.staff_division_id)
        
        vacancy = self.model() # init object
        
        vacancy.position_id = position.id
        vacancy.staff_division_id = staff_division.id
        
        
        if body.hr_vacancy_requirements_ids is not None:
            vacancy_requirements = []
            
            for requirement in body.hr_vacancy_requirements_ids:
                requirement = hr_vacancy_requirement_service.get_by_id(db, requirement)
            
                vacancy_requirements.append(requirement)
            
            vacancy.hr_vacancy_requirements = vacancy_requirements
        
        
        db.add(vacancy)
        db.flush()
        
        return vacancy
    
    
    def get_candidates(self, db: Session, id: str, role_id: str) -> List[StaffUnit]:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        vacancy = self.get_by_id(db, id)
        
        return vacancy.hr_vacancy_candidates
    
    
    def respond_to_vacancy(self, db: Session, id: str, user_id: str):
        
        current_user = user_service.get_by_id(db, user_id)
        
        vacancy = self.get_by_id(db, id)
        
        if current_user not in vacancy.hr_vacancy_candidates:
            vacancy.hr_vacancy_candidates.append(current_user)
        
        return vacancy


    def unactive(self, db: Session, id: str, role_id: str) -> HrVacancy:
        
        if not self._check_by_role(db, role_id):
            raise ForbiddenException("You don't have permission to manage vacancy!")
        
        vacancy = self.get_by_id(db, id)
        
        vacancy.is_active = False
        
        db.add(vacancy)
        db.flush()
        
        return vacancy


    def _check_by_role(self, db: Session, role_id: str) -> bool:
        current_user_staff_unit = staff_unit_service.get_by_id(db, role_id)
        current_user_position = current_user_staff_unit.position
        
        if current_user_position.name != PositionNameEnum.HR:
            return False
        
        return True

hr_vacancy_service = HrVacancyService(HrVacancy)
