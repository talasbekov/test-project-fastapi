import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    HrVacancyRequirementsRead,
    HrVacancyRequirementsCreate,
    HrVacancyRequirementsUpdate
)
from services import hr_vacancy_requirement_service

router = APIRouter(
    prefix="/hr_vacancy_requirements",
    tags=["HrVacancyRequirements"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrVacancyRequirementsRead],
            summary="Get all HrVacancyRequirements")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all HrVacancyRequirements

       - **skip**: int - The number of HrVacancyRequirements
        to skip before returning the results.
        This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of HrVacancyRequirements
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return hr_vacancy_requirement_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HrVacancyRequirementsRead,
             summary="Create HrVacancyRequirements")
async def create(*,
                 body: HrVacancyRequirementsCreate,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return hr_vacancy_requirement_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRequirementsRead,
            summary="Get HrVacancyRequirements by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get HrVacancyRequirements by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_vacancy_requirement_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrVacancyRequirementsRead,
            summary="Update HrVacancyRequirements")
async def update(*,
                 id: uuid.UUID,
                 body: HrVacancyRequirementsUpdate,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    hr_vacancy_requirement = hr_vacancy_requirement_service.get_by_id(db, str(id))
    return hr_vacancy_requirement_service.update(
        db, db_obj=hr_vacancy_requirement, obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete HrVacancyRequirements")
async def delete(*,
                 id: uuid.UUID,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    hr_vacancy_requirement_service.remove(db, str(id))
