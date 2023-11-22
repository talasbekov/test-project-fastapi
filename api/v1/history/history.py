import datetime
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HistoryCreate, HistoryUpdate, HistoryRead,
                     HistoryServiceDetailRead, HistoryContractCreate,
                     HistoryBadgeCreate, HistorySecondmentCreate,
                     HistoryPenaltyCreate, HistoryStatusCreate,
                     HistoryCoolnessCreate, HistoryAttestationCreate,
                     HistoryBlackBeretCreate)
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
                           date_to: datetime.date = None,
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
        db, user_id, date_from, date_to, skip, limit)


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


@router.post("/contract", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Contract History")
async def create_contract_history(*,
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
    return history_service.create_contract_history(db, body)


@router.post("/bagde", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Badge History")
async def create_badge_history(*,
                               db: Session = Depends(get_db),
                               body: HistoryBadgeCreate,
                               Authorize: AuthJWT = Depends()
                               ):
    """
        Create badge history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_badge_history(db, body)

@router.post("/black_beret", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Black Beret History")
async def create_black_beret_history(*,
                               db: Session = Depends(get_db),
                               body: HistoryBlackBeretCreate,
                               Authorize: AuthJWT = Depends()
                               ):
    """
        Create badge history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_black_beret_history(db, body)


@router.post("/secondement", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Secondment History")
async def create_secondement_history(*,
                                     db: Session = Depends(get_db),
                                     body: HistorySecondmentCreate,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
        Create secondment history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_secondment_history(db, body)


@router.post("/penalty", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Penalty History")
async def create_penalty_history(*,
                                 db: Session = Depends(get_db),
                                 body: HistoryPenaltyCreate,
                                 Authorize: AuthJWT = Depends()
                                 ):
    """
        Create penalty history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_penalty_history(db, body)


@router.post("/status", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Status History")
async def create_status_history(*,
                                db: Session = Depends(get_db),
                                body: HistoryStatusCreate,
                                Authorize: AuthJWT = Depends()
                                ):
    """
        Create status history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_status_history(db, body)


@router.post("/coolness", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Coolness History")
async def create_coolness_history(*,
                                  db: Session = Depends(get_db),
                                  body: HistoryCoolnessCreate,
                                  Authorize: AuthJWT = Depends()
                                  ):
    """
        Create status history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_coolness_history(db, body)


@router.post("/attestation", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HistoryRead,
             summary="Create Attestation History")
async def create_attestation_history(*,
                                     db: Session = Depends(get_db),
                                     body: HistoryAttestationCreate,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
        Create attestation history

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.create_attestation_history(db, body)


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

@router.put("/secondment/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Update History")
async def update_secondment(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: HistoryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update secondment history

        - **id**: UUID - the id of history to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.update_secondment(db, id, body)

@router.put("/badge/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Update History")
async def update_badge(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: HistoryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update badge history

        - **id**: UUID - the id of history to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.update_badge(db, id, body)

@router.put("/status/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HistoryRead,
            summary="Update History")
async def update_status(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: HistoryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update badge history

        - **id**: UUID - the id of history to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return history_service.update_status(db, id, body)

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
    
@router.delete("/black_beret/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Black Beret History")
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
    history_service.black_beret_remove(db, str(id))


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
                                      date_till: datetime.date = None,
                                      Authorize: AuthJWT = Depends(),
                                      ):
    """
        Get timeline for user id

        - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    if date_till is not None:
        date_till = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        return history_service.get_timeline_by_date(db, user_id, date_till)
    return history_service.get_timeline(db, user_id)
