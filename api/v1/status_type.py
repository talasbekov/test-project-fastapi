import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import StatusTypeCreate, StatusTypeUpdate, StatusTypeRead, StatusTypePaginationRead
from services import status_type_service

router = APIRouter(
    prefix="/status_types",
    tags=["Status types"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=StatusTypePaginationRead,
            summary="Get all Status types")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Status types

       - **skip**: int - The number of Status types
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Status types
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return status_type_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StatusTypeRead,
             summary="Create Status type")
async def create(*,
                 db: Session = Depends(get_db),
                 body: StatusTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Status type

        - **name**: required
    """
    Authorize.jwt_required()
    return status_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StatusTypeRead,
            summary="Get Status type by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Status type by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return status_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StatusTypeRead,
            summary="Update Status type")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: StatusTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Status type

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return status_type_service.update(
        db,
        db_obj=status_type_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Status type")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Status type

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    status_type_service.remove(db, str(id))
