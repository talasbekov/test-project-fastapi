import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from models import PermissionTypeEnum
from core import get_db

from schemas import (AdditionalProfileCreate,
                     AdditionalProfileRead,
                     AdditionalProfileUpdate)

from services import additional_profile_service, profile_service

router = APIRouter(
    prefix="/additional-profile",
    tags=["Additional Profile"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AdditionalProfileRead],
            summary="Get all Additional Profile")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
    Get all Abroad Travel

    - **skip**: int - The number of abroad travel to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of abroad travel to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return additional_profile_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AdditionalProfileCreate,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends(),
                 user_id: str
                 ):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    profile = profile_service.get_by_user_id(db, str(user_id))
    return additional_profile_service.create(db, {"profile_id": profile.id})


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AdditionalProfileRead,
            summary="Update Abroad Travel by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: AdditionalProfileUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = additional_profile_service.get_by_id(db, str(id))
    return additional_profile_service.update(db, abroad_travel, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=AdditionalProfileRead,
               summary="Delete Abroad Travel by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = additional_profile_service.get_by_id(db, str(id))
    return additional_profile_service.delete(db, abroad_travel)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AdditionalProfileRead,
            summary="Get Additional Profile by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get additional profile by id

        - **name**: required
    """
    Authorize.jwt_required()
    return additional_profile_service.get_by_id(db, str(id))


@router.get("/profile", response_model=AdditionalProfileRead)
async def get_profile(*,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()
                      ):
    Authorize.jwt_required()
    profile = profile_service.get_by_user_id(db, Authorize.get_jwt_subject())
    return additional_profile_service.get_by_id(
        db, profile.additional_profile.id)


@router.get('/profile/{id}/', response_model=AdditionalProfileRead)
async def get_profile_by_id(*,
                            db: Session = Depends(get_db),
                            id: str,
                            Authorize: AuthJWT = Depends()
                            ):
    Authorize.jwt_required()
    permissions = Authorize.get_raw_jwt()['permissions']
    res = profile_service.get_by_user_id(db, str(id)).additional_profile
    res = AdditionalProfileRead.from_orm(res).dict()
    if id != Authorize.get_jwt_subject():
    # res = res.__dict__
        if int(PermissionTypeEnum.VIEW_SPEC_INSPECTIONS.value) not in permissions:
            res['special_checks'] = "Permission Denied"
        if int(PermissionTypeEnum.VIEW_POLIGRAPH.value) not in permissions:
            res['polygraph_checks'] = "Permission Denied"
        if int(PermissionTypeEnum.VIEW_VIOLATIONS.value) not in permissions:
            res['violations'] = "Permission Denied"
        if int(PermissionTypeEnum.VIEW_PSYCH_CHARACTERISTICS.value) not in permissions:
            res['psychological_checks'] = "Permission Denied"
    return res
