import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ExamScheduleRead,
                     ExamScheduleUpdate,
                     ExamScheduleCreateWithInstructors,
                     ExamResultReadPagination)

from services import exam_service


router = APIRouter(prefix="/exam",
                   tags=["ExamSchedule"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=ExamResultReadPagination,
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
    return exam_service.get_exam_results_by_user_id(db, user_id, skip, limit)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Get ExamSchedule by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
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
    return exam_service.create(db, body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ExamScheduleRead,
            summary="Update ExamSchedule")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
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
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete ExamSchedule

    """
    Authorize.jwt_required()
    return exam_service.remove(db, str(id))
