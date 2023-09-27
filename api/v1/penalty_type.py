import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import PenaltyTypeCreate, PenaltyTypeUpdate, PenaltyTypeRead, PenaltyTypePaginationRead
from services import penalty_type_service

router = APIRouter(
    prefix="/penalty_types",
    tags=["Penalty types"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=PenaltyTypePaginationRead,
            summary="Get all Penalty types")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Penalty types

       - **skip**: int - The number of Penalty types
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Penalty types
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return penalty_type_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PenaltyTypeRead,
             summary="Create Penalty type")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PenaltyTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Penalty type

        - **name**: required
    """
    Authorize.jwt_required()
    return penalty_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PenaltyTypeRead,
            summary="Get Penalty type by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Penalty type by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return penalty_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PenaltyTypeRead,
            summary="Update Penalty type")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PenaltyTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Penalty type

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return penalty_type_service.update(
        db,
        db_obj=penalty_type_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Penalty type")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Penalty type

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    penalty_type_service.remove(db, str(id))
