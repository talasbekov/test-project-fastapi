import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import SportDegreeTypeCreate, SportDegreeTypeRead, SportDegreeTypeUpdate, SportDegreeTypePaginationRead
from services import sport_degree_type_service

router = APIRouter(
    prefix="/sport_degree_type",
    tags=["SportDegreeType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=SportDegreeTypePaginationRead,
            summary="Get all SportDereeTypes")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SportDegreeTypes

        - **skip**: int - The number of SportType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of SportType
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return sport_degree_type_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SportDegreeTypeRead,
             summary="Create SportDegreeType")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SportDegreeTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new SportDegreeType

        - **name**: str
    """
    Authorize.jwt_required()
    return sport_degree_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportDegreeTypeRead,
            summary="Get SportDegreeType by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get SportDegreeType by id
    """
    Authorize.jwt_required()
    return sport_degree_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportDegreeTypeRead,
            summary="Update SportDegreeType by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: SportDegreeTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update SportDegreeType by id

        - **name**: str
    """
    Authorize.jwt_required()
    return sport_degree_type_service.update(
        db, db_obj=sport_degree_type_service.get_by_id(db, str(id)), obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=SportDegreeTypeRead,
               summary="Delete SportDegreeType by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete SportDegreeType by id
    """
    Authorize.jwt_required()
    return sport_degree_type_service.remove(db, str(id))
