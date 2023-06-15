import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HrVacancyRead, HrVacancyCreate, HrVacancyCandidateRead,
                     HrVacancyStaffDivisionRead)
from schemas.hr_vacancy import HrVacancyUpdate
from services import hr_vacancy_service

router = APIRouter(prefix="/hr_vacancies", tags=["HrVacancies"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrVacancyRead],
            summary="Get all HrVacancies")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Get all HrVacancies
    """
    Authorize.jwt_required()
    return hr_vacancy_service.get_multi(db)


@router.get("/department/{staff_division_id}", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyStaffDivisionRead,
            summary="Get all HrVacancies by department")
async def get_all_by_department(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    staff_division_id: uuid.UUID
):
    """
        Get all HrVacancies by department
        
        - **staff_division_id**: uuid - required.
    """
    Authorize.jwt_required()
    return hr_vacancy_service.get_by_department(db, staff_division_id)


@router.get("/not_active", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrVacancyRead],
            summary="Get all not active HrVacancies")
async def get_not_active(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all HrVacancies

       - **skip**: int - The number of HrVacancies to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of HrVacancies to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return hr_vacancy_service.get_multi_not_active(db, skip, limit)


@router.get("/{id}/candidates", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrVacancyCandidateRead],
            summary="Get all candidates of Vacancy")
async def get_all_candidates(*,
    id: uuid.UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Get all Candidates of HrVacancy
        
       - **id**: uuid - the id of HrVacancy.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return hr_vacancy_service.get_candidates(db, id, role)


@router.post("/{id}/respond", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Respond to Candidate (Отклик)")
async def respond(*,
    id: uuid.UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Respond to the Hrvacancy

       - **id**: uuid - the id of HrVacancy.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_vacancy_service.respond_to_vacancy(db, id, user_id)


@router.post("", status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Create HrVacancy")
async def create(*,
    body: HrVacancyCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Create HrVacancy
        
        - **staff_unit_id**: uuid - required
        - **hr_vacancy_requirements_ids**: List of uuid - optional
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return hr_vacancy_service.create(db, body, role)


@router.post("/archieve-staff-unit", status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Create HrVacancy by archieve staff unit")
async def create_by_archieve_staff_unit(*,
    body: HrVacancyCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Create HrVacancy by archieve staff unit
        
        - **staff_unit_id**: uuid - required. The id of ArchieveStaffUnit
        - **hr_vacancy_requirements_ids**: List of uuid - optional
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return hr_vacancy_service.create_by_archive_staff_unit(db, body, role)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Update HrVacancy")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrVacancyUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HrVacancy
        
        - **id**: uuid - required
        - **archive_staff_unit_id**: uuid - optional. The id of ArchiveStaffUnit
        - **staff_unit_id**: uuid - optional. The id of StaffUnit
        - **is_active**: bool - optional
        - **hr_vacancy_requirements_ids**: List of uuid - optional
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    hr_vacancy = hr_vacancy_service.get_by_id(db, id)
    return hr_vacancy_service.update(db, hr_vacancy, body, role)


@router.put("/{id}/archieve-staff-unit", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Update HrVacancy")
async def update_by_archieve_staff_unit(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrVacancyUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HrVacancy
        
        - **id**: uuid - required
        - **archive_staff_unit_id**: uuid - optional. The id of ArchiveStaffUnit
        - **staff_unit_id**: uuid - optional. The id of StaffUnit
        - **is_active**: bool - optional
        - **hr_vacancy_requirements_ids**: List of uuid - optional
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return hr_vacancy_service.update(db, id, body, role)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Get HrVacancy by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrVacancy by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_vacancy_service.get_by_id(db, id)


@router.get("/archieve-staff-unit/{archieve_staff_unit_id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRead,
            summary="Get HrVacancy by archieve staff unit")
async def get_by_archieve_staff_unit_id(*,
    db: Session = Depends(get_db),
    archieve_staff_unit_id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrVacancy by archieve staff unit

        - **archieve_staff_unit_id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_vacancy_service.get_by_archieve_staff_unit(db, archieve_staff_unit_id)

