import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    IdentificationCardCreate,
    IdentificationCardUpdate,
    IdentificationCardRead
)
from services import identification_card_service

router = APIRouter(
    prefix="/identification_card",
    tags=["IdentificationCard"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[IdentificationCardRead],
            summary="Get all IdentificationCard")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all IdentificationCard

        - **skip**: int - The number of IdentificationCard
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of IdentificationCard
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return identification_card_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=IdentificationCardRead,
             summary="Create IdentificationCard")
async def create(*,
                 db: Session = Depends(get_db),
                 body: IdentificationCardCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new IdentificationCard

        - **document_number**: str
        - **date_of_issue**: datetime.date
        - **date_to: datetime**.date
        - **issued_by**: str
        - **document_link**: str
        - **profile_id**: str
    """
    Authorize.jwt_required()
    return identification_card_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=IdentificationCardRead,
            summary="Get IdentificationCard by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get IdentificationCard by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return identification_card_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=IdentificationCardRead,
            summary="Update IdentificationCard")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: IdentificationCardUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update IdentificationCard

        - **id**: UUID - the ID of IdentificationCard to update. This is required.
        - **document_link**: str (url)
    """
    Authorize.jwt_required()
    return identification_card_service.update(
        db,
        db_obj=identification_card_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete IdentificationCard")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete IdentificationCard

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    identification_card_service.remove(db, str(id))
