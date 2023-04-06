import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import CoolnessCreate, CoolnessUpdate, CoolnessRead
from services import coolness_service
from models import SpecialityEnum


router = APIRouter(prefix="/coolness", tags=["Coolness"], dependencies=[Depends(HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CoolnessRead],
            summary="Get all Privelege Emergencies")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
       Get all Military Units

       - **skip**: int - The number of Military Units to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Military Units to return in the response. This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return coolness_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CoolnessRead,
             summary="Create Military Unit")
async def create(*,
    db: Session = Depends(get_db),
    body: CoolnessCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Military Unit

        **name** - required - str
    """
    Authorize.jwt_required()
    return coolness_service.create(db, body)


@router.get("/forms/", dependencies=[Depends(HTTPBearer())],
            summary="Get all Speciality Enum")
async def get_all_forms(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    """
       Get all Speciality Enum
   """
    Authorize.jwt_required()
    return [speciality_enum.value for speciality_enum in SpecialityEnum]

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SpecialityEnum,
            summary="Update Privelege Emergency")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: SpecialityEnum,
    Authorize: AuthJWT = Depends()
):
    """
        Update Privelege Emergency

        **name** - required - str
    """
    Authorize.jwt_required()
    privelege_emergency = coolness_service.get_by_id(db, id)
    return coolness_service.update(db, db_obj=privelege_emergency, obj_in=body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessRead,
            summary="Get Privelege Emergency Unit by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Privelege Emergency by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return coolness_service.get_by_id(db, id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Privelege Emergency ")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Military Unit

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    coolness_service.remove(db, id=id)
