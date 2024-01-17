import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (CoolnessTypeCreate,
                     CoolnessTypeRead,
                     CoolnessTypeUpdate,
                     CoolnessTypeReadPagination,)
from services import coolness_type_service


router = APIRouter(
    prefix="/coolness_type",
    tags=["Coolness Type"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessTypeReadPagination,
            summary="Get all Coolness")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Coolness

    - **skip**: int - The number of Coolness to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Coolness to return in the response.
        This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return coolness_type_service.get_all(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CoolnessTypeRead,
             summary="Create Coolness Type")
async def create(*,
                 db: Session = Depends(get_db),
                 body: CoolnessTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Coolness

        **name** - required - str
    """
    Authorize.jwt_required()
    return coolness_type_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessTypeRead,
            summary="Update Coolness Type")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: CoolnessTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Coolness

        **name** - required - str
    """
    Authorize.jwt_required()
    coolness = coolness_type_service.get_by_id(db, str(id))
    return coolness_type_service.update(db, db_obj=coolness, obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessTypeRead,
            summary="Get Coolness by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Coolness by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return coolness_type_service.get_by_id(db, str(id))


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Coolness ")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Coolness

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    coolness_type_service.remove(db, id=id)
