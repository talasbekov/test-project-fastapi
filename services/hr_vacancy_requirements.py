from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import HrVacancyRequirements

from schemas import HrVacancyRequirementsCreate, HrVacancyRequirementsUpdate
from .base import ServiceBase


class HrVacancyRequirementService(
        ServiceBase[HrVacancyRequirements, HrVacancyRequirementsCreate, HrVacancyRequirementsUpdate]):

    def get_by_id(self, db: Session, id: str):

        hr_vacancy_requirement = super().get(db, id)
        if hr_vacancy_requirement is None:
            raise NotFoundException(
                detail=f"HrVacancyRequirements with id: {id} is not found!")
        return hr_vacancy_requirement


hr_vacancy_requirement_service = HrVacancyRequirementService(
    HrVacancyRequirements)
