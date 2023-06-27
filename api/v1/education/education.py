import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (EducationCreate,
                               EducationRead,
                               EducationUpdate)
from services.education import education_service

router = APIRouter(prefix="/educations",
                   tags=["Educations"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[EducationRead],
            summary="Get all Educations")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Educations

    - **skip**: int - The number of Educations
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Educations
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return education_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=EducationRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: EducationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Education

        - **name**: required
    """
    Authorize.jwt_required()
    return education_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EducationRead,
            summary="Get Education by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Education by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return education_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EducationRead,
            summary="Update Education")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: EducationUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Education

        - **id**: UUID - the ID of Education to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return education_service.update(
        db,
        db_obj=education_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Education")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Education

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    education_service.remove(db, id)
