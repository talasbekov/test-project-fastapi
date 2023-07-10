import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import FamilyStatusRead
from services import family_status_service

router = APIRouter(
    prefix="/family_status",
    tags=["FamilyStatus"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[FamilyStatusRead],
            summary="Get all FamilyStatus")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all FamilyStatus

        - **skip**: int - The number of FamilyStatus
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of FamilyStatus
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return family_status_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyStatusRead,
            summary="Get FamilyStatus by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get FamilyStatus by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return family_status_service.get_by_id(db, id)


@router.get('/user/{user_id}', dependencies=[Depends(HTTPBearer())],
            response_model=FamilyStatusRead)
async def get_profile_by_id(*,
                            db: Session = Depends(get_db),
                            user_id: uuid.UUID,
                            Authorize: AuthJWT = Depends()
                            ):
    Authorize.jwt_required()
    return family_status_service.get_by_user_id(db, user_id)
