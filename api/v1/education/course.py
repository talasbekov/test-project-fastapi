import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (CourseCreate,
                               CourseRead,
                               CourseUpdate)
from services.education import course_service

router = APIRouter(prefix="/courses",
                   tags=["Courses"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CourseRead],
            summary="Get all Courses")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Courses

        - **skip**: int - The number of Courses to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Courses to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return course_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CourseRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: CourseCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new Course

        - **name**: required
    """
    Authorize.jwt_required()
    return course_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CourseRead,
            summary="Get Course by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Course by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return course_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CourseRead,
            summary="Update Course")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: CourseUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Course

        - **id**: UUID - the ID of Course to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return course_service.update(
        db,
        db_obj=course_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Course")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Course

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    course_service.remove(db, id)
