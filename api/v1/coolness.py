import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import CoolnessCreate, CoolnessRead
from services import coolness_service
from models import SpecialtyEnum


router = APIRouter(
    prefix="/coolness",
    tags=["Coolness"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CoolnessRead],
            summary="Get all Coolness")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Coolness

    - **skip**: int - The number of Coolness to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Coolness to return in the response.
        This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return coolness_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CoolnessRead,
             summary="Create Coolness")
async def create(*,
                 db: Session = Depends(get_db),
                 body: CoolnessCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Coolness

        **name** - required - str
    """
    Authorize.jwt_required()
    return coolness_service.create(db, body)


@router.get("/forms/", dependencies=[Depends(HTTPBearer())],
            summary="Get all Specialty Enum")
async def get_all_forms(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
   """
    Authorize.jwt_required()
    return [specialty_enum.value for specialty_enum in SpecialtyEnum]


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessRead,
            summary="Update Coolness")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: SpecialtyEnum,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Coolness

        **name** - required - str
    """
    Authorize.jwt_required()
    coolness_emergency = coolness_service.get_by_id(db, id)
    return coolness_service.update(db, db_obj=coolness_emergency, obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CoolnessRead,
            summary="Get Coolness by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Coolness by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return coolness_service.get_by_id(db, id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Coolness ")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Coolness

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    coolness_service.remove(db, id=id)
