import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import CountryCreate, CountryUpdate, CountryRead, CountryReadPagination
from services import country_service

router = APIRouter(
    prefix="/country",
    tags=["Country"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=CountryReadPagination,
            summary="Get all Country")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Country

        - **skip**: int - The number of country to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of country to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return country_service.get_all(db, skip, limit, filter)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CountryRead,
            summary="Get Country by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get country by id
    """
    Authorize.jwt_required()
    return country_service.get_by_id(db, str(id))


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CountryRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: CountryCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new country

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return country_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CountryRead,
            summary="Update")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: CountryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update country

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    country = country_service.get_by_id(db, str(id))
    return country_service.update(db, db_obj=country, obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=CountryRead,
               summary="Delete")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete country
    """
    Authorize.jwt_required()
    return country_service.remove(db, str(id))
