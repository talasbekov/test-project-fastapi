import datetime
import json
import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ExamScheduleRead,
                     ExamScheduleUpdate,
                     ExamScheduleCreateWithInstructors,
                     ExamResultReadPagination,
                     ExamScheduleReadPagination,
                     ExamChangeResults,
                     ExamResultRead,
                     ExamTabletRead,)

from services import exam_service, exam_result_service


router = APIRouter(prefix="/exam",
                   tags=["ExamSchedule"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleReadPagination,
            summary="Get all ExamSchedule")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ExamSchedule

    - **skip**: int - The number of ExamSchedule
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ExamSchedule
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return exam_service.get_multi(db, skip, limit)

@router.get("/tablet/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamTabletRead,
            summary="Get all ExamSchedule")
async def get_for_tablet(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ExamSchedule

    - **skip**: int - The number of ExamSchedule
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ExamSchedule
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return exam_service.get_for_tablet(db, skip, limit)

@router.get("/users/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=List[ExamResultRead],
            summary="Get ExamSchedule users by id")
async def get_exam_users(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ExamSchedule users by id
    """
    Authorize.jwt_required()
    return exam_result_service.get_users_results_by_exam(db, id)

@router.get("/results/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamResultReadPagination,
            summary="Get ExamSchedule by id")
async def get_exam_results(*,
                    db: Session = Depends(get_db),
                    skip: int = 0,
                    limit: int = 100,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ExamResults by authorized user

    - **skip**: int - The number of ExamSchedule
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ExamSchedule
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return exam_result_service.get_exam_results_by_user_id(db, user_id, skip, limit)

@router.get("/month", dependencies=[Depends(HTTPBearer())],
            response_model=List[ExamScheduleRead],
            summary="Get ScheduleMonths by month")
async def get_by_month(*,
                      db: Session = Depends(get_db),
                      month_num: int = 1,
                      Authorize: AuthJWT = Depends()
                      ):
    """
       Get ScheduleMonths by month

    - **month**: int - The number of month when you want to get ScheduleMonth
   """

    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return exam_service.get_exams_by_month(db, user_id, month_num)

@router.get("/nearest", dependencies=[Depends(HTTPBearer())],
            response_model=List[ExamScheduleRead],
            summary="Get nearest ScheduleMonths")
async def get_nearest(*,
                      db: Session = Depends(get_db),
                      limit: int = 100,
                      Authorize: AuthJWT = Depends()
                      ):
    """
       Get nearest ScheduleMonths

    - **limit**: int - The maximum number of ScheduleMonth
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return exam_service.get_nearest_exams(db, user_id, limit)

@router.get("/date", dependencies=[Depends(HTTPBearer())],
            response_model=List[ExamScheduleRead],
            summary="Get ScheduleMonths by date")
async def get_by_date(*,
                      db: Session = Depends(get_db),
                      limit: int = 100,
                      date: datetime.date,
                      Authorize: AuthJWT = Depends()
                      ):
    """
       Get ScheduleMonths by date

    - **limit**: int - The maximum number of ScheduleMonth
        to return in the response.
        This parameter is optional and defaults to 100.
    - **date**: date (yyyy-mm-dd) - The date when you want to get ScheduleMonth
   """

    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return exam_service.get_exams_by_day(db, user_id, date, limit)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Get ExamSchedule by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ExamSchedule by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return exam_service.get_by_id(db, str(id))

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Create ExamSchedule")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ExamScheduleCreateWithInstructors,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create ExamSchedule

    """
    Authorize.jwt_required()
    exam_schedule = exam_service.create(db, body)
    users = exam_service.get_users_by_exam(db, exam_schedule.id)
    exam_result_service.create_exam_results_by_exam(db, exam_schedule.id, users)
    for group in exam_schedule.schedule.staff_divisions:
        if isinstance(group.description, str):
            group.description = json.loads(group.description)
    return exam_schedule

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Update ExamSchedule")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ExamScheduleUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ExamSchedule

    """
    Authorize.jwt_required()
    return exam_service.update(
        db,
        db_obj=exam_service.get_by_id(db, str(id)),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Delete ExamSchedule")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete ExamSchedule

    """
    Authorize.jwt_required()
    return exam_service.remove(db, id)

@router.put("/results_update", dependencies=[Depends(HTTPBearer())],
            summary="Change Exam Results")
async def change_results(*,
                 db: Session = Depends(get_db),
                 body: ExamChangeResults,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Change Exam Results
    """
    Authorize.jwt_required()
    exam_service.get_by_id(db, str(body.exam_id))
    exam_result_service.change_exam_results(db, body)
