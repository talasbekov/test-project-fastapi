import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (EducationalProfileCreate,
                     EducationalProfileRead,
                     EducationalProfileUpdate)
from services import profile_service
from services.education import educational_profile_service

router = APIRouter(prefix="/educational_profiles",
                   tags=["EducationalProfiles"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=None,
            summary="Get all EducationalProfiles")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all EducationalProfiles

        - **skip**: int - The number of EducationalProfiles to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of EducationalProfiles to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return educational_profile_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=EducationalProfileRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: EducationalProfileCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new EducationalProfile

        - **name**: required
    """
    Authorize.jwt_required()
    return educational_profile_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EducationalProfileRead,
            summary="Get EducationalProfile by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get EducationalProfile by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return educational_profile_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EducationalProfileRead,
            summary="Update EducationalProfile")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: EducationalProfileUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update EducationalProfile

        - **id**: UUID - the ID of EducationalProfile to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return educational_profile_service.update(
        db,
        db_obj=educational_profile_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete EducationalProfile")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete EducationalProfile

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    educational_profile_service.remove(db, id)


@router.get("/profile", dependencies=[Depends(HTTPBearer())],
            response_model=EducationalProfileRead)
async def get_profile(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    print(profile.educational_profile.language_proficiency)
    return educational_profile_service.get_by_id(db, profile.educational_profile.id)


@router.get("/profile/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=EducationalProfileRead)
async def get_profile_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return profile_service.get_by_user_id(db, id).educational_profile
