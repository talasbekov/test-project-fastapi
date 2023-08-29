import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ScheduleDayRead,
                     ScheduleDayUpdate,
                     ScheduleDayCreate,)

from services import schedule_day_service


router = APIRouter(prefix="/schedule_day",
                   tags=["ScheduleDay"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleDayRead],
            summary="Get all ScheduleDay")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ScheduleDay

    - **skip**: int - The number of ScheduleDay
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ScheduleDay
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return schedule_day_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleDayRead,
            summary="Get ScheduleDay by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ScheduleDay by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return schedule_day_service.get_by_id(db, str(id))

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleDayRead,
            summary="Create ScheduleDay")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ScheduleDayCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create ScheduleDay

    """
    Authorize.jwt_required()
    return schedule_day_service.create(db, obj_in=body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleDayRead,
            summary="Update ScheduleDay")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ScheduleDayUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ScheduleDay

    """
    Authorize.jwt_required()
    return schedule_day_service.update(
        db,
        db_obj=schedule_day_service.get_by_id(db, str(id)),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleDayRead,
            summary="Delete ScheduleDay")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete ScheduleDay

    """
    Authorize.jwt_required()
    return schedule_day_service.remove(db, id)
