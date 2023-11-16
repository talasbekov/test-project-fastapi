import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (InstitutionDegreeTypeCreate,
                               InstitutionDegreeTypeRead,
                               InstitutionDegreeTypeUpdate,
                               InstitutionDegreeTypeReadPagination,)
from services.education import institution_degree_type_service

router = APIRouter(prefix="/institution_degree_types",
                   tags=["InstitutionDegreeTypes"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=InstitutionDegreeTypeReadPagination,
            summary="Get all InstitutionDegreeTypes")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all InstitutionDegreeTypes

    - **skip**: int - The number of InstitutionDegreeTypes
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of InstitutionDegreeTypes
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return institution_degree_type_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=InstitutionDegreeTypeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: InstitutionDegreeTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new InstitutionDegreeType

        - **name**: required
    """
    Authorize.jwt_required()
    return institution_degree_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=InstitutionDegreeTypeRead,
            summary="Get InstitutionDegreeType by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get InstitutionDegreeType by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return institution_degree_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=InstitutionDegreeTypeRead,
            summary="Update InstitutionDegreeType")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: InstitutionDegreeTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update InstitutionDegreeType

        - **id**: UUID - the ID of InstitutionDegreeType to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return institution_degree_type_service.update(
        db,
        db_obj=institution_degree_type_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete InstitutionDegreeType")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete InstitutionDegreeType

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    institution_degree_type_service.remove(db, str(id))
