import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import RegionCreate, RegionUpdate, RegionRead
from services import region_service


router = APIRouter(
    prefix="/region",
    tags=["Region"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[RegionRead],
                summary="Get all Region")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Region

        - **skip**: int - The number of Region
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Region
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return region_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=RegionRead,
                summary="Create Region")
async def create(*,
                db: Session = Depends(get_db),
                body: RegionCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new Region
    """
    Authorize.jwt_required()
    return region_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=RegionRead,
                summary="Get Region by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Region by ID
    """
    Authorize.jwt_required()
    return region_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=RegionRead,
                summary="Update Region by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: RegionUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update Region by ID
    """
    Authorize.jwt_required()
    Region = region_service.get_by_id(db, id)
    return region_service.update(db, db_obj=Region, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=RegionRead,
                summary="Delete Region by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete Region by ID
    """
    Authorize.jwt_required()
    return region_service.remove(db, id)

@router.get("/get_by_country/{country_id}", dependencies=[Depends(HTTPBearer())],
                response_model=List[RegionRead],
                summary="Get Region by Country ID")
async def get_by_country_id(*,
                            db: Session = Depends(get_db),
                            country_id: str,
                            Authorize: AuthJWT = Depends()
                            ):
    """
        Get Region by Country ID
    """
    Authorize.jwt_required()
    return region_service.get_region_by_country_id(db, country_id)
