import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (AcademicDegreeCreate,
                               AcademicDegreeRead,
                               AcademicDegreeUpdate)
from services.education import academic_degree_service

router = APIRouter(prefix="/academic_degrees",
                   tags=["AcademicDegrees"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AcademicDegreeRead],
            summary="Get all AcademicDegrees")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all AcademicDegrees

        - **skip**: int - The number of AcademicDegrees
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of AcademicDegrees
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return academic_degree_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AcademicDegreeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AcademicDegreeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new AcademicDegree

        - **name**: required
    """
    Authorize.jwt_required()
    return academic_degree_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeRead,
            summary="Get AcademicDegree by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get AcademicDegree by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return academic_degree_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeRead,
            summary="Update AcademicDegree")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AcademicDegreeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update AcademicDegree

        - **id**: UUID - the ID of AcademicDegree to update.
            This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return academic_degree_service.update(
        db,
        db_obj=academic_degree_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AcademicDegree")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete AcademicDegree

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    academic_degree_service.remove(db, id)
