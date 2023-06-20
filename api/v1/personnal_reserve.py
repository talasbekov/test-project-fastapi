import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    PersonnalReserveRead, 
    PersonnalReserveCreate, 
    PersonnalReserveUpdate
)
from services import personnal_reserve_service
from models import ReserveEnum


router = APIRouter(
    prefix="/personnal_reserve",
    tags=["PersonnalReserve"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PersonnalReserveRead],
            summary="Get all Privelege Emergencies")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Military Units

       - **skip**: int - The number of Military Units 
            to skip before returning the results. 
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Military Units 
            to return in the response. 
            This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return personnal_reserve_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PersonnalReserveRead,
             summary="Create Military Unit")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PersonnalReserveCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Military Unit

        **name** - required - str
    """
    Authorize.jwt_required()
    return personnal_reserve_service.create(db, body)


@router.get("/forms/", dependencies=[Depends(HTTPBearer())],
            summary="Get all Reserve Enum")
async def get_all_forms(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Privelege Emergency Forms
   """
    Authorize.jwt_required()
    return [reserve.name for reserve in ReserveEnum]


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PersonnalReserveRead,
            summary="Update Privelege Emergency")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: PersonnalReserveUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Privelege Emergency

        **name** - required - str
    """
    Authorize.jwt_required()
    personnal_reserve = personnal_reserve_service.get_by_id(db, id)
    return personnal_reserve_service.update(db, personnal_reserve, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PersonnalReserveRead,
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
    return personnal_reserve_service.get_by_id(db, id)


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
    personnal_reserve_service.remove(db, id)
