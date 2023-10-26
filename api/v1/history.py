from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import HistoryCreate, HistoryUpdate, HistoryRead, HistoryContractCreate
from services import history_service

router = APIRouter(
    prefix="/histories",
    tags=["Histories"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HistoryRead],
            summary="Get all Histories")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
        Get all Histories

        - **skip**: int - The number of Historys to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Historys to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return history_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create History")
async def create(*,
                 db: Session = Depends(get_db),
                 body: HistoryCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create History

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create(db, body)


@router.post("/contract/", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Contract History")
async def create_contract(*,
                          db: Session = Depends(get_db),
                          body: HistoryContractCreate,
                          Authorize: AuthJWT = Depends()
                          ):
    """
        Create contract history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_contract(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Get History by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
       Get History by id

       - **id**: UUID - required
    """
    Authorize.jwt_required()
    return history_service.get_by_id(db, str(id))

# get all by type


@router.get("/type/{type}/", dependencies=[Depends(HTTPBearer())],
            response_model=List[HistoryRead],
            summary="Get all Histories by type")
async def get_all_by_type(*,
                          db: Session = Depends(get_db),
                          type: str,
                          Authorize: AuthJWT = Depends(),
                          skip: int = 0,
                          limit: int = 10
                          ):
    """
        Get all Histories by type

        - **type**: str - required
        - **skip**: int - The number of Historys to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Historys to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return history_service.get_all_by_type(db, type, skip, limit)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Update History")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: HistoryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update History

        - **id**: UUID - the id of History to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.update(db, id, body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete History")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete History

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    history_service.remove(db, str(id))
