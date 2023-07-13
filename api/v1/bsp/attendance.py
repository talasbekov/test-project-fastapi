import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (AttendanceRead,
                     AttendanceUpdate,
                     AttendanceCreate,)

from services import attendance_service


router = APIRouter(prefix="/attendance",
                   tags=["Attendance"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AttendanceRead],
            summary="Get all Attendance")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Attendance

    - **skip**: int - The number of Attendance
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Attendance
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return attendance_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendanceRead,
            summary="Get Attendance by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Attendance by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return attendance_service.get_by_id(db, id)

@router.get("/percentage", dependencies=[Depends(HTTPBearer())],
            response_model=List[dict],
            summary="Get Attendance by id")
async def get_attendance_percentage(*,
                    db: Session = Depends(get_db),
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Attendance by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return attendance_service.get_percentage_by_user_id(db, user_id)

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendanceRead,
            summary="Create Attendance")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AttendanceCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Attendance

    """
    Authorize.jwt_required()
    return attendance_service.create(db, obj_in=body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendanceRead,
            summary="Update Attendance")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AttendanceUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Attendance

    """
    Authorize.jwt_required()
    return attendance_service.update(
        db,
        db_obj=attendance_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendanceRead,
            summary="Delete Attendance")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Attendance

    """
    Authorize.jwt_required()
    return attendance_service.remove(db, id)
