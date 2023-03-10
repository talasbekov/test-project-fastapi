import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import ServiceHousingCreate, ServiceHousingUpdate, ServiceHousingRead
from services import service_housing_service


router = APIRouter(prefix="/service-housings", tags=["Service Housings"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceHousingRead],
            summary="Get all Service Housings")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Service Housings

        - **skip**: int - The number of Service Housings to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Service Housings to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return service_housing_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=ServiceHousingRead,
                summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: ServiceHousingCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return service_housing_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceHousingRead,
            summary="Update")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: ServiceHousingUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Service Housing

        - **id**: required
        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return service_housing_service.update(db, service_housing_service.get_by_id(id), body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceHousingRead,
            summary="Delete")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Service Housing

        - **id**: required
    """
    Authorize.jwt_required()
    return service_housing_service.remove(db, id)
