import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (PersonalProfileCreate, PersonalProfileRead,
                     PersonalProfileUpdate)
from services import personal_profile_service, profile_service

router = APIRouter(prefix="/personal_profile", tags=["PersonalProfile"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PersonalProfileRead],
            summary="Get all PersonalProfiles")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all PersonalProfiles

        - **skip**: int - The number of PersonalProfiles to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of PersonalProfiles to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return personal_profile_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PersonalProfileRead,
             summary="Create PersonalProfiles")
async def create(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
        Create new PersonalProfiles

        no parameters required
    """
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    return personal_profile_service.create(db, {"profile_id": profile.id})


@router.get("/profile", response_model=PersonalProfileRead)
async def get_profile(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    return profile.personal_profile


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PersonalProfileRead,
            summary="Get PersonalProfiles by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get PersonalProfiles by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return personal_profile_service.get_by_id(db, id)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete PersonalProfiles")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete PersonalProfiles

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    personal_profile_service.remove(db, id)
