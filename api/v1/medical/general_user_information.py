import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import GeneralUserInformationRead,GeneralUserInformationCreate,GeneralUserInformationUpdate
from services.medical import general_user_information_service

router = APIRouter(prefix="/general_user_information", tags=["General User Information"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[GeneralUserInformationRead],
            summary="Get all General User Information")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all General User Information
        - **skip**: int - The number of General User Information to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of General User Information to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return general_user_information_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=GeneralUserInformationRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: GeneralUserInformationCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new General User Information
        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return general_user_information_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=GeneralUserInformationRead,
            summary="Get General User Information by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get General User Information by id
        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return general_user_information_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model= GeneralUserInformationRead,
            summary="Update General User Information")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: GeneralUserInformationUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update General User Information
        - **id**: UUID - the ID of General User Information to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return general_user_information_service.update(
        db,
        db_obj=general_user_information_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete General User Information")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete a General User Information 
        - **id**: UUId - required
    """
    Authorize.jwt_required()
    general_user_information_service.remove(db, id)
