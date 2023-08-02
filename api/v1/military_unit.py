import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import MilitaryUnitCreate, MilitaryUnitRead, MilitaryUnitUpdate
from services import military_unit_service

router = APIRouter(
    prefix="/military_units",
    tags=["MilitaryUnit"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[MilitaryUnitRead],
            summary="Get all Military Units")
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
    return military_unit_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=MilitaryUnitRead,
             summary="Create Military Unit")
async def create(*,
                 db: Session = Depends(get_db),
                 body: MilitaryUnitCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Military Unit

        **name** - required - str
    """
    Authorize.jwt_required()
    return military_unit_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=MilitaryUnitRead,
            summary="Update Military Unit")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: MilitaryUnitUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Military Unit

        **name** - required - str
    """
    Authorize.jwt_required()
    return military_unit_service.update(
        db=db,
        db_obj=military_unit_service.get_by_id(db, str(id)),
        obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=MilitaryUnitRead,
            summary="Get Military Unit by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Military Unit by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return military_unit_service.get_by_id(db, str(id))


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Military Unit")
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
    military_unit_service.remove(db, str(id))
