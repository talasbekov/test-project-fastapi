import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HistoryNameChangeCreate,
                     HistoryNameChangeUpdate,
                     HistoryNameChangeRead)
from services import history_name_change_service

router = APIRouter(prefix="/history/name_change",
                   tags=["History Name Change"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HistoryNameChangeRead],
            summary="Get all History Name Changes")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
        Get all History Name Changes

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return history_name_change_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryNameChangeRead,
             summary="Create History Name Change")
async def create(*,
                 db: Session = Depends(get_db),
                 body: HistoryNameChangeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create History Name Change

        - **name**: str - required
        - **type**: str - required
    """
    Authorize.jwt_required()
    return history_name_change_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryNameChangeRead,
            summary="Get History by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
       Get Equipment by id

       - **id**: UUID - required
    """
    Authorize.jwt_required()
    return history_name_change_service.get_by_id(db, id)


@router.get("/user/{user_id}/", dependencies=[Depends(HTTPBearer())],
            summary="Get History Name Changes by user id")
async def get_by_user_id(*,
                         db: Session = Depends(get_db),
                         user_id: str,
                         Authorize: AuthJWT = Depends()
                         ):
    """
       Get History Name Changes by user id

       - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    return history_name_change_service.get_all_by_user_id(db, user_id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryNameChangeRead,
            summary="Update History")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: HistoryNameChangeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Equipment

        - **id**: UUID - the id of equipment to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    history_name_change = history_name_change_service.get_by_id(db, id)
    return history_name_change_service.update(db,
                                              db_obj=history_name_change,
                                              obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete History Name Change")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete History Name Change

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    history_name_change_service.remove(db, id)
