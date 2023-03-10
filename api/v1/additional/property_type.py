from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas import PropertyTypeCreate, PropertyTypeRead, PropertyTypeUpdate
from core import get_db
from services import property_type_service, profile_service
from exceptions import ForbiddenException, SgoErpException
from typing import List
import uuid

router = APIRouter(prefix="/properties", tags=["Properties"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PropertyTypeRead],
            summary="Get all Properties")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Properties

        - **skip**: int - The number of Properties to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Properties to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject() 
    return property_type_service.get_multi_by_user_id(db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=PropertyTypeRead,
                summary="Create")


async def create(*,
    db: Session = Depends(get_db),
    body: PropertyTypeCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()  
    profile = profile_service.get_by_user_id(db, credentials)
    body.profile_id = profile.additional_profile.id
    return property_type_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PropertyTypeRead,
            summary="Update Abroad Travel by id")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: PropertyTypeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject() 
    profile = profile_service.get_by_user_id(db, credentials)
    abroad_travel = property_type_service.get_by_id(db, id)
    if abroad_travel.profile_id != profile.id: # TODO: check role logic
        raise SgoErpException("You don't have permission to update this properties")
    return property_type_service.update(db, abroad_travel, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PropertyTypeRead,
            summary="Delete properties by id")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete properties by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    profile = profile_service.get_by_user_id(db, credentials)
    properties = property_type_service.get_by_id(db, id)
    if properties.profile_id != profile.id: # TODO: check role logic
        raise ForbiddenException("You don't have permission to delete these properties")
    return property_type_service.delete(db, properties)
