import uuid

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import PersonalProfileCreate, PersonalProfileUpdate, PersonalProfileRead
from services import personal_profile_service

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

    """
    Authorize.jwt_required()
    return personal_profile_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PersonalProfileRead,
             summary="Create PersonalProfiles")
async def create(*,
    db: Session = Depends(get_db),
    body: PersonalProfileCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new PersonalProfiles

    """
    Authorize.jwt_required()
    return personal_profile_service.create(db, body)

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


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PersonalProfileRead,
            summary="Update PersonalProfiles")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: PersonalProfileUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update PersonalProfiles

    """
    Authorize.jwt_required()
    return personal_profile_service.update(
        db,
        db_obj=personal_profile_service.get_by_id(db, id),
        obj_in=body)


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
