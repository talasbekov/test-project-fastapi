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
from models import PermissionTypeEnum
from services import profile_service, dispensary_registration_service, user_liberations_service, hospital_data_service
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
    permissions = Authorize.get_raw_jwt()['permissions']
    profile = profile_service.get_by_user_id(
        db, str(id))
    
    medical_profile = profile.medical_profile
    medical_profile_id = medical_profile_service.get_by_profile_id(db, profile.id).id

    dispensary_registrations = dispensary_registration_service.get_by_profile_id(db, medical_profile_id)
    user_liberations = user_liberations_service.get_by_profile_id(db, medical_profile_id)
    hospital_datas = hospital_data_service.get_by_profile_id(db, medical_profile_id)
    # print('HHHHEEEERREEE')
    # print(medical_profile_id, hospital_datas.__dict__)

    medical_profile.dispensary_registrations = dispensary_registrations
    medical_profile.hospital_datas = hospital_datas
    medical_profile.user_liberations = user_liberations

    medical_profile = MedicalProfileRead.from_orm(medical_profile).dict()
    if medical_profile['user_liberations'] is not None:
        for user_liberation in medical_profile['user_liberations']:
            user_liberation['liberation_ids'] = medical_profile_service.get_liberation_ids(
                db, user_liberation)
    if id != Authorize.get_jwt_subject():
        if int(PermissionTypeEnum.VIEW_DISP_UCHET.value) not in permissions:
            medical_profile['dispensary_registrations'] = "Permission Denied"
        if int(PermissionTypeEnum.VIEW_LEAVES.value) not in permissions:
            medical_profile['user_liberations'] = "Permission Denied"
        if int(PermissionTypeEnum.VIEW_MEDICAL_LISTS.value) not in permissions:
            medical_profile['hospital_datas'] = "Permission Denied"
    return medical_profile
