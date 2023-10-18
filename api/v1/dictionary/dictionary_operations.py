from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import JoinRecordsBody
from services import dictionary_service

router = APIRouter(
    prefix="/operations",
    tags=["Dictionary operations"],
    dependencies=[Depends(HTTPBearer())])


@router.post("/join_records", dependencies=[Depends(HTTPBearer())],
             status_code=status.HTTP_200_OK,
             summary="Join records")
async def join_records(*,
                       db: Session = Depends(get_db),
                       entity: str,
                       body: JoinRecordsBody,
                       Authorize: AuthJWT = Depends()
                       ) -> str:
    """
       Change all records with ids_to_change to correct_id

       - **entity**: str - table where records will be joined
       - **correct_id**: str - id that will have updated records.
       - **ids_to_change**: str - ids that will be switched by
            correct_id
    """
    Authorize.jwt_required()
    await dictionary_service.join_records(db, entity, body)
    return "Records successfully updated"


@router.post("/soft_update", dependencies=[Depends(HTTPBearer())],
             status_code=status.HTTP_200_OK,
             summary="Soft update record")
async def soft_update(*,
                      db: Session = Depends(get_db),
                      entity: str,
                      id: str,
                      Authorize: AuthJWT = Depends()
                      ) -> str:
    """
       Change all records with ids_to_change to correct_id

       - **entity**: str - entity which records will be soft updated
       - **id**: str - id to update
    """
    Authorize.jwt_required()
    obj_id = await dictionary_service.soft_update(db, entity, id)
    return obj_id
