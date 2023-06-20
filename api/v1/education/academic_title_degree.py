import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (AcademicTitleDegreeCreate,
                               AcademicTitleDegreeRead,
                               AcademicTitleDegreeUpdate)
from services.education import academic_title_degree_service

router = APIRouter(prefix="/academic_title_degrees",
                   tags=["AcademicTitleDegrees"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AcademicTitleDegreeRead],
            summary="Get all AcademicTitleDegrees")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all AcademicTitleDegrees

    - **skip**: int - The number of AcademicTitleDegrees 
        to skip before returning the results. 
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of AcademicTitleDegrees 
        to return in the response. 
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return academic_title_degree_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AcademicTitleDegreeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AcademicTitleDegreeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new AcademicTitleDegree

        - **name**: required
    """
    Authorize.jwt_required()
    return academic_title_degree_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicTitleDegreeRead,
            summary="Get AcademicTitleDegree by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get AcademicTitleDegree by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return academic_title_degree_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicTitleDegreeRead,
            summary="Update AcademicTitleDegree")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AcademicTitleDegreeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update AcademicTitleDegree

        - **id**: UUID - the ID of AcademicTitleDegree to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return academic_title_degree_service.update(
        db,
        db_obj=academic_title_degree_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AcademicTitleDegree")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete AcademicTitleDegree

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    academic_title_degree_service.remove(db, id)
