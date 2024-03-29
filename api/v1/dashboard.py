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


@router.get("/states/all", dependencies=[Depends(HTTPBearer())],
            summary="Get all data for Dashboard")
async def get_all_state(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Количество всей штатки
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_all_state(db, role)


@router.get("/states/by_list/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data by list for Dashboard")
async def get_state_by_list(*,
                            db: Session = Depends(get_db),
                            Authorize: AuthJWT = Depends(),
                            ):
    """
       Количество сотрудников по списку
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_state_by_list(db, role)


@router.get("/states/vacancies/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of vacancies for Dashboard")
async def get_hr_vacancy_count_by_division(*,
                                           db: Session = Depends(get_db),
                                           Authorize: AuthJWT = Depends(),
                                           ):
    """
       Количество вакансии
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_hr_vacancy_count_by_division(db, role)


@router.get("/states/inline/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of users in line for Dashboard")
async def get_in_line_count_by_status(*,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends(),
                                      ):
    """
       Количество сотрудников которые в строю
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_in_line_count_by_status(db, role)


@router.get("/states/outline/all/", dependencies=[Depends(HTTPBearer())],
            summary="Get data of all out line users for Dashboard")
async def get_count_by_status_all_users(*,
                                        db: Session = Depends(get_db),
                                        Authorize: AuthJWT = Depends(),
                                        ):
    """
       Общее количество сотрудников которые отсутствуют
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_count_by_status_all_users(db, role)


@router.get("/states/outline/bystatus/", dependencies=[Depends(HTTPBearer())],
            summary="Get data by every status of out line users for Dashboard")
async def get_count_by_every_status_users(*,
                                          db: Session = Depends(get_db),
                                          Authorize: AuthJWT = Depends(),
                                          ):
    """
       Количество сотрудников которые отсутствуют по статусам
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_count_by_every_status_users(db, role)


@router.get("/candidates/active/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of active candidates for Dashboard")
async def get_all_active_candidates(*,
                                    db: Session = Depends(get_db),
                                    Authorize: AuthJWT = Depends(),
                                    ):
    """
       Количество изучающихся кандидатов
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_all_active_candidates(db, role)


@router.get("/candidates/stages", dependencies=[Depends(HTTPBearer())],
            summary="Get passed candidate stage infos")
async def get_statistic_passed_candidate_stage_infos(*,
                                                     db: Session = Depends(
                                                         get_db),
                                                     Authorize: AuthJWT = Depends(),
                                                     ):
    """
       Get passed candidate stage infos
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return (
        dashboard_service.get_statistic_passed_candidate_stage_infos(db, role)
    )


@router.get("/candidates/duration", dependencies=[Depends(HTTPBearer())],
            summary="Get duration candidates")
async def get_statistic_duration_candidate_learning(*,
                                                    db: Session = Depends(
                                                        get_db),
                                                    Authorize: AuthJWT = Depends(),
                                                    ):
    """
       Get duration candidates
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return (
        dashboard_service.get_statistic_duration_candidate_learning(db, role)
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


@router.get("/candidates/curators/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of candidates curators for Dashboard")
async def get_curators_by_candidates(*,
                                     db: Session = Depends(get_db),
                                     Authorize: AuthJWT = Depends(),
                                     ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dict(dashboard_service.get_curators_by_candidates(db, role))


@router.get("/candidates/curators/duration", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of candidates curators for Dashboard")
async def get_curators_by_candidates_duration(*,
                                              db: Session = Depends(get_db),
                                              Authorize: AuthJWT = Depends(),
                                              ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dict(dashboard_service.get_curators_by_candidates_duration(db, role))


@router.get("/users/all/inErp", dependencies=[Depends(HTTPBearer())],
            summary="All users in ecosystem ERP")
async def get_all_users_of_erp(*,
                               db: Session = Depends(get_db),
                               Authorize: AuthJWT = Depends(),
                               ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    return dashboard_service.get_all_users_of_erp(db)


@router.get("/users/added", dependencies=[Depends(HTTPBearer())],
            summary="How match users are added")
async def get_all_new_users_at_week(*,
                                    db: Session = Depends(get_db),
                                    Authorize: AuthJWT = Depends(),
                                    ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    return dashboard_service.get_all_new_users_at_week(db)


@router.get("/users/active", dependencies=[Depends(HTTPBearer())],
            summary="Online users")
async def get_all_active(*,
                         db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends(),
                         ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    return dashboard_service.get_active_users(db)


@router.get("/users/active/statistics", dependencies=[Depends(HTTPBearer())],
            summary="Get all data of users activity by three days")
async def get_users_at_three_day_by_active(*,
                                           db: Session = Depends(get_db),
                                           Authorize: AuthJWT = Depends(),
                                           ):
    """
       Количество изучающих кандидатов кураторы
    """
    Authorize.jwt_required()
    return dashboard_service.get_users_at_three_day_by_active(db)
