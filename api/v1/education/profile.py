import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import ProfileCreate, ProfileRead, ProfileUpdate
from services.education import profile_service

router = APIRouter(prefix="/academic_degrees", tags=["Profiles"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ProfileRead],
            summary="Get all Profiles")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Profiles

        - **skip**: int - The number of Profiles to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Profiles to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return profile_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ProfileRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: ProfileCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new Profile

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return profile_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ProfileRead,
            summary="Get Profile by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Profile by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return profile_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ProfileRead,
            summary="Update Profile")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: ProfileUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Profile

        - **id**: UUID - the ID of Profile to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return profile_service.update(
        db,
        db_obj=profile_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Profile")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Profile

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    profile_service.remove(db, id)


@router.get("/help")
async def help(*,
    db: Session = Depends(get_db)):
    profile_service.add_Profile(db, ProfileCreate(name="test", url="sad"))
    raise Exception('help')
