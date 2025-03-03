import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import CityCreate, CityUpdate, CityRead
from services import city_service


router = APIRouter(
    prefix="/city",
    tags=["City"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[CityRead],
                summary="Get all City")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all City

        - **skip**: int - The number of City
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of City
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return city_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=CityRead,
                summary="Create City")
async def create(*,
                db: Session = Depends(get_db),
                body: CityCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new City
    """
    Authorize.jwt_required()
    return city_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CityRead,
                summary="Get City by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get City by ID
    """
    Authorize.jwt_required()
    return city_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CityRead,
                summary="Update City by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: CityUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update City by ID
    """
    Authorize.jwt_required()
    City = city_service.get_by_id(db, id)
    return city_service.update(db, db_obj=City, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CityRead,
                summary="Delete City by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete City by ID
    """
    Authorize.jwt_required()
    return city_service.remove(db, id)

@router.get("/get_by_region/{region_id}", dependencies=[Depends(HTTPBearer())],
                response_model=List[CityRead],
                summary="Get City by Region ID")
async def get_by_region_id(*,
                            db: Session = Depends(get_db),
                            region_id: str,
                            Authorize: AuthJWT = Depends()
                            ):
    """
        Get City by Region ID
    """
    Authorize.jwt_required()
    return city_service.get_cities_by_region_id(db, region_id)    

@router.get("/get_by_country/{country_id}", dependencies=[Depends(HTTPBearer())],
                response_model=List[CityRead],
                summary="Get City by Country ID")
async def get_by_country_id(*,
                            db: Session = Depends(get_db),
                            country_id: str,
                            Authorize: AuthJWT = Depends()
                            ):
    """
        Get City by Country ID
    """
    Authorize.jwt_required()
    return city_service.get_cities_by_country_id(db, country_id)