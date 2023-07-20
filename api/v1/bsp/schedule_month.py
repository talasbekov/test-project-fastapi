import datetime
import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ScheduleMonthRead,
                     ScheduleMonthUpdate,
                     ScheduleMonthCreateWithDay,)

from services import schedule_month_service


router = APIRouter(prefix="/schedule_month",
                   tags=["ScheduleMonth"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleMonthRead],
            summary="Get all ScheduleMonth")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ScheduleMonth

    - **skip**: int - The number of ScheduleMonth
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ScheduleMonth
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return schedule_month_service.get_multi(db, skip, limit)


@router.get("/nearest", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleMonthRead],
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
    return schedule_month_service.get_nearest_schedules(db, user_id, limit)


@router.get("/date", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleMonthRead],
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
    return schedule_month_service.get_schedule_by_day(db, user_id, date, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleMonthRead,
            summary="Get ScheduleMonth by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ScheduleMonth by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return schedule_month_service.get_by_id(db, id)

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleMonthRead,
            summary="Create ScheduleMonth")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ScheduleMonthCreateWithDay,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create ScheduleMonth

    """
    Authorize.jwt_required()
    return schedule_month_service.create(db, body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleMonthRead,
            summary="Update ScheduleMonth")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: ScheduleMonthUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ScheduleMonth

    """
    Authorize.jwt_required()
    return schedule_month_service.update(
        db,
        db_obj=schedule_month_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleMonthRead,
            summary="Delete ScheduleMonth")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete ScheduleMonth

    """
    Authorize.jwt_required()
    return schedule_month_service.remove(db, id)
