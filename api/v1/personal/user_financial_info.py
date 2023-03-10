import uuid

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserFinancialInfoCreate, UserFinancialInfoUpdate, UserFinancialInfoRead
from services import user_financial_info_service

router = APIRouter(prefix="/user_financial_info", tags=["UserFinancialInfo"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[UserFinancialInfoRead],
            summary="Get all UserFinancialInfo")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all UserFinancialInfo

        - **skip**: int - The number of UserFinancialInfo to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of UserFinancialInfo to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return user_financial_info_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserFinancialInfoRead,
             summary="Create UserFinancialInfo")
async def create(*,
    db: Session = Depends(get_db),
    body: UserFinancialInfoCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new UserFinancialInfo

        - **iban**: str
        - **housing_payments_iban**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return user_financial_info_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserFinancialInfoRead,
            summary="Get UserFinancialInfo by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get UserFinancialInfo by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return user_financial_info_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserFinancialInfoRead,
            summary="Update UserFinancialInfo")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: UserFinancialInfoUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update UserFinancialInfo

        - **id**: UUID - the ID of UserFinancialInfo to update. This is required.
        - **iban**: str
        - **housing_payments_iban**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return user_financial_info_service.update(
        db,
        db_obj=user_financial_info_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete UserFinancialInfo")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete UserFinancialInfo

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_financial_info_service.remove(db, id)
