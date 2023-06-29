import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (InstitutionCreate,
                               InstitutionRead,
                               InstitutionUpdate)
from services.education import institution_service

router = APIRouter(prefix="/institutions",
                   tags=["Institutions"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[InstitutionRead],
            summary="Get all Institutions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Institutions

    - **skip**: int - The number of Institutions
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Institutions
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return institution_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=InstitutionRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: InstitutionCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Institution

        - **name**: required
    """
    Authorize.jwt_required()
    return institution_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=InstitutionRead,
            summary="Get Institution by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Institution by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return institution_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=InstitutionRead,
            summary="Update Institution")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: InstitutionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Institution

        - **id**: UUID - the ID of Institution to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return institution_service.update(
        db,
        db_obj=institution_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Institution")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Institution

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    institution_service.remove(db, id)
