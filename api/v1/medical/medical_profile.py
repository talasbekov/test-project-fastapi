import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import (
    MedicalProfileCreate,
    MedicalProfileRead,
    MedicalProfileUpdate
)
from services import profile_service
from services.medical import medical_profile_service

router = APIRouter(
    prefix="/medical_profile",
    tags=["MedicalProfile"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[MedicalProfileRead],
            summary="Get all MedicalProfile")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Medical Profile

    - **skip**: int - The number of MedicalProfile
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of MedicalProfile
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return medical_profile_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=MedicalProfileRead,
             summary="Create MedicalProfile")
async def create(*,
                 db: Session = Depends(get_db),
                 body: MedicalProfileCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new MedicalProfile

        - **profile_id**: str
    """
    Authorize.jwt_required()
    return medical_profile_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=MedicalProfileRead,
            summary="Get MedicalProfile by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get MedicalProfile by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return medical_profile_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=MedicalProfileRead,
            summary="Update MedicalProfile")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: MedicalProfileUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Medical Profile

        - **id**: UUID - the ID of MedicalProfile to update. This is required.
        - **profile_id**: str
    """
    Authorize.jwt_required()
    return medical_profile_service.update(
        db,
        db_obj=medical_profile_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete MedicalProfile")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete a MedicalProfile

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    medical_profile_service.remove(db, str(id))


@router.get("/profile", response_model=MedicalProfileRead)
async def get_profile(*,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()
                      ):
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    return medical_profile_service.get_by_id(db, profile.medical_profile.id)


@router.get("/profile/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=MedicalProfileRead)
async def get_profile_by_id(*,
                            db: Session = Depends(get_db),
                            id: str,
                            Authorize: AuthJWT = Depends()
                            ):
    Authorize.jwt_required()
    return profile_service.get_by_user_id(db, str(id)).medical_profile
