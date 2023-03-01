import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import JurisdictionCreate, JurisdictionUpdate, JurisdictionRead
from services import jurisdiction_service

router = APIRouter(prefix="/jurisdictions", tags=["Jurisdictions"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[JurisdictionRead],
            summary="Get all Jurisdictions")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all Jurisdictions

       - **skip**: int - The number of Jurisdictions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Jurisdictions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return jurisdiction_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=JurisdictionRead,
             summary="Create Jurisdiction")
async def create(*,
    db: Session = Depends(get_db),
    body: JurisdictionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Jurisdiction

        - **name**: required
    """
    Authorize.jwt_required()
    return jurisdiction_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=JurisdictionRead,
            summary="Get Jurisdiction by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Jurisdiction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return jurisdiction_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=JurisdictionRead,
            summary="Update Jurisdiction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: JurisdictionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Jurisdiction

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return jurisdiction_service.update(
        db,
        db_obj=jurisdiction_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Jurisdiction")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Jurisdiction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    jurisdiction_service.remove(db, id)
