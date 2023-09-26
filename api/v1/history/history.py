import datetime
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import HistoryCreate, HistoryUpdate, HistoryRead, HistoryServiceDetailRead
from services import history_service
from models import HistoryEnum

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

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return history_service.get_all(db, skip, limit)

# get enums


@router.get("/enums", dependencies=[Depends(HTTPBearer())],
            response_model=List[str],
            summary="Get all History Enums")
async def get_all_enums(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends()
                        ):
    """
        Get all History Enums
    """
    Authorize.jwt_required()
    return [e.value for e in HistoryEnum]


@router.get("/personal/{user_id}", dependencies=[Depends(HTTPBearer())],
            summary="Get all Histories by user id")
async def get_all_personal(*,
                           db: Session = Depends(get_db),
                           user_id: str,
                           Authorize: AuthJWT = Depends(),
                           date_from: datetime.date = None,
                           skip: int = 0,
                           limit: int = 10
                           ):
    """
        Get all Histories by user id

        - **user_id**: UUID - required
        - **date_from**: date - format (YYYY-MM). This parameter is optional.
    """
    Authorize.jwt_required()
    return history_service.get_all_personal(
        db, user_id, date_from, skip, limit)


@router.get("/user/{user_id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryServiceDetailRead,
            summary="Get all Service and Details by user id")
async def get_all_by_user_id(*,
                             db: Session = Depends(get_db),
                             user_id: str,
                             Authorize: AuthJWT = Depends()
                             ):
    """
        Get all Histories by user id

        - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    return history_service.get_all_by_user_id(db, str(user_id))


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Equipment")
async def create(*,
                 db: Session = Depends(get_db),
                 body: HistoryCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Equipment

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Get History by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
       Get Equipment by id

       - **id**: UUID - required
    """
    Authorize.jwt_required()
    return history_service.get_by_id(db, str(id))

# get all by type


@router.get("/type/{type}/", dependencies=[Depends(HTTPBearer())],
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
        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
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
        Update Equipment

        - **id**: UUID - the id of equipment to update. This parameter is required
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
        Delete Equipment

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    history_service.remove(db, str(id))


@router.get("/all/type/{type}/{user_id}", dependencies=[Depends(HTTPBearer())],
            summary="Get all Histories by type and user id")
async def get_all_by_type_and_user_id(*,
                                      db: Session = Depends(get_db),
                                      type: str,
                                      user_id: str,
                                      Authorize: AuthJWT = Depends(),
                                      skip: int = 0,
                                      limit: int = 10
                                      ):
    """
        Get all Histories by type and user id

        - **type**: str - required
        - **user_id**: UUID - required
        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return history_service.get_all_by_type_and_user_id(
        db, type, user_id, skip, limit)

@router.get("/timeline", dependencies=[Depends(HTTPBearer())],
            summary="Get all Histories by type and user id")
async def get_all_by_type_and_user_id(*,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends(),
                                      ):
    """
        Get timeline for user id
        
        - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return history_service.get_timeline(db, user_id)
