import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ScheduleYearRead,
                     ScheduleYearUpdate,
                     ScheduleYearCreateString,)

from services import schedule_year_service, plan_service


router = APIRouter(prefix="/schedule_year",
                   tags=["ScheduleYear"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleYearRead],
            summary="Get all ScheduleYear")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ScheduleYear

    - **skip**: int - The number of ScheduleYear
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ScheduleYear
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return schedule_year_service.get_multi(db, skip, limit)

@router.get("/plan/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleYearRead],
            summary="Get all ScheduleYear by plan id")
async def get_all_by_plan(*,
                  db: Session = Depends(get_db),
                  id: uuid.UUID,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ScheduleYears by plan id

    - **skip**: int - The number of ScheduleYear
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ScheduleYear
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    plan_service.get_by_id(db, id)
    return schedule_year_service.get_all_by_plan_id(db, id)

@router.get("/staff_division/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleYearRead],
            summary="Get all ScheduleYear by staff_division id")
async def get_all_by_staff_division(*,
                  db: Session = Depends(get_db),
                  id: uuid.UUID,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ScheduleYears by plan id

   """
    Authorize.jwt_required()
    return schedule_year_service.get_all_by_division_id(db, id)

@router.get("/year/", dependencies=[Depends(HTTPBearer())],
            response_model=List[ScheduleYearRead],
            summary="Get all Schedule Year by plan year")
async def get_all_by_year(*,
                  db: Session = Depends(get_db),
                  year: int = 2000,
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Schedule Year by plan year

    - **year**: int - year on which to get the schedule
    - **skip**: int - The number of ScheduleYear
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of ScheduleYear
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return schedule_year_service.get_all_by_plan_year(db, year, skip, limit)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleYearRead,
            summary="Get ScheduleYear by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ScheduleYear by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return schedule_year_service.get_by_id(db, id)

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleYearRead,
            summary="Create ScheduleYear")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ScheduleYearCreateString,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create ScheduleYear

    """
    Authorize.jwt_required()
    return schedule_year_service.create_schedule(db, body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleYearRead,
            summary="Update ScheduleYear")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: ScheduleYearUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ScheduleYear

    """
    Authorize.jwt_required()
    return schedule_year_service.update(
        db,
        db_obj=schedule_year_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScheduleYearRead,
            summary="Delete ScheduleYear")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete ScheduleYear

    """
    Authorize.jwt_required()
    return schedule_year_service.remove(db, id)
