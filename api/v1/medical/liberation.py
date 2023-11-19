import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import (
    LiberationCreate,
    LiberationRead,
    LiberationUpdate,
    LiberationReadPagination
)
from services.medical import liberation_service

router = APIRouter(
    prefix="/liberations",
    tags=["Liberation"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=LiberationReadPagination,
            summary="Get all Liberation")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Liberation

    - **skip**: int - The number of Liberation
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Liberation
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return liberation_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=LiberationRead,
             summary="Create Liberation")
async def create(*,
                 db: Session = Depends(get_db),
                 body: LiberationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Liberation

        - **name**: str -required
    """
    Authorize.jwt_required()
    return liberation_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LiberationRead,
            summary="Get Liberation by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Hospital Data by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return liberation_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LiberationRead,
            summary="Update Liberation")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: LiberationUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Liberation

        - **id**: UUID - required.
        - **name**: str -required
    """
    Authorize.jwt_required()
    return liberation_service.update(
        db,
        db_obj=liberation_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Liberation")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete a Liberation

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    liberation_service.remove(db, str(id))
