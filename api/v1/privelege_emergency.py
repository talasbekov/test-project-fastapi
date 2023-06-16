import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import PrivelegeEmergencyRead, PrivelegeEmergencyCreate, PrivelegeEmergencyUpdate
from services import privelege_emergency_service
from models import FormEnum


router = APIRouter(
    prefix="/privelege_emergencies",
    tags=["PrivelegeEmergency"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PrivelegeEmergencyRead],
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
    return privelege_emergency_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PrivelegeEmergencyRead,
             summary="Create Military Unit")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PrivelegeEmergencyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Military Unit

        **name** - required - str
    """
    Authorize.jwt_required()
    return privelege_emergency_service.create(db, body)


@router.get("/forms/", dependencies=[Depends(HTTPBearer())],
            summary="Get all Privelege Emergency Forms")
async def get_all_forms(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Privelege Emergency Forms
   """
    Authorize.jwt_required()
    return [form.value for form in FormEnum]


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PrivelegeEmergencyRead,
            summary="Update Privelege Emergency")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: PrivelegeEmergencyUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Privelege Emergency

        **name** - required - str
    """
    Authorize.jwt_required()
    privelege_emergency = privelege_emergency_service.get_by_id(db, id)
    return privelege_emergency_service.update(db, privelege_emergency, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PrivelegeEmergencyRead,
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
    return privelege_emergency_service.get_by_id(db, id)


@router.get("/user/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PrivelegeEmergencyRead,
            summary="Get Privelege Emergency Unit by user id")
async def get_by_user_id(*,
                         db: Session = Depends(get_db),
                         id: uuid.UUID,
                         Authorize: AuthJWT = Depends()
                         ):
    """
        Get Privelege Emergency by user id

        - **user_id** - UUID - required
    """
    Authorize.jwt_required()
    return privelege_emergency_service.get_by_user_id(db, id)


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
    privelege_emergency_service.remove(db, id)
