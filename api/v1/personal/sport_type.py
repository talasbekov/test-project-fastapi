import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import SportTypeCreate, SportTypeRead, SportTypeUpdate, SportTypePaginationRead
from services import sport_type_service

router = APIRouter(
    prefix="/sport_type",
    tags=["SportType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=SportTypePaginationRead,
            summary="Get all SportType")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SportType

        - **skip**: int - The number of SportType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of SportType
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return sport_type_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SportTypeRead,
             summary="Create SportType")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SportTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new SportType

        - **name**: str
    """
    Authorize.jwt_required()
    return sport_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportTypeRead,
            summary="Get SportType by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get SportType by id
    """
    Authorize.jwt_required()
    return sport_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportTypeRead,
            summary="Update SportType by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: SportTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update SportType by id

        - **name**: str
    """
    Authorize.jwt_required()
    return sport_type_service.update(
        db, db_obj=sport_type_service.get_by_id(db, str(id)), obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=SportTypeRead,
               summary="Delete SportType by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete SportType by id
    """
    Authorize.jwt_required()
    return sport_type_service.remove(db, str(id))
