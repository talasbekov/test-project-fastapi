from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from services import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("/states/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data for Dashboard")
async def get_all_state(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_all_state(db, role)


@router.get("/statebylist/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data by list for Dashboard")
async def get_state_by_list(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_state_by_list(db, role)


@router.get("/vacancies/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of vacancies for Dashboard")
async def get_hr_vacancy_count_by_division(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_hr_vacancy_count_by_division(db, role)


@router.get("/inline/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of users in line for Dashboard")
async def get_in_line_count_by_status(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_in_line_count_by_status(db, role)

@router.get("/candidates/stages", dependencies=[Depends(HTTPBearer())],
            summary="Get passed candidate stage infos")
async def get_statistic_passed_candidate_stage_infos(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get passed candidate stage infos
    """
    Authorize.jwt_required()
    return (
       dashboard_service.get_statistic_passed_candidate_stage_infos(db)
    )

@router.get("/candidates/duration", dependencies=[Depends(HTTPBearer())],
            summary="Get duration candidates")
async def get_statistic_duration_candidate_learning(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get duration candidates
    """
    Authorize.jwt_required()
    return (
       dashboard_service.get_statistic_duration_candidate_learning(db)
    )

@router.get("/candidates/completed", dependencies=[Depends(HTTPBearer())],
            summary="Get completed candidates")
async def get_statistic_completed_candidates(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get completed candidates
    """
    Authorize.jwt_required()
    return (
       dashboard_service.get_statistic_completed_candidates(db)
    )