import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import FamilyProfileCreate, FamilyProfileRead, FamilyProfileUpdate
from services import family_profile_service, profile_service

router = APIRouter(
    prefix="/family_profiles",
    tags=["Family Profile"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[FamilyProfileRead])
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    Authorize.jwt_required()
    return family_profile_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=FamilyProfileRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: FamilyProfileCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return family_profile_service.create(db, obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyProfileRead)
async def get(*,
              db: Session = Depends(get_db),
              id: uuid.UUID,
              Authorize: AuthJWT = Depends()
              ):
    Authorize.jwt_required()
    return family_profile_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyProfileRead)
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: FamilyProfileUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return family_profile_service.update(
        db, db_obj=family_profile_service.get_by_id(db, id), obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    family_profile_service.remove(db, id=id)


@router.get("/profile", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyProfileRead)
async def get_by_profile(*,
                         db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends()
                         ):
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    return profile.family_profile


@router.get('/profile/{id}/', dependencies=[Depends(HTTPBearer())],
            response_model=FamilyProfileRead)
async def get_by_profile_id(*,
                            db: Session = Depends(get_db),
                            id: uuid.UUID,
                            Authorize: AuthJWT = Depends()
                            ):
    Authorize.jwt_required()
    return profile_service.get_by_user_id(db, id).family_profile
