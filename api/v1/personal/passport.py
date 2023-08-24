import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import PassportCreate, PassportUpdate, PassportRead
from services import passport_service

router = APIRouter(
    prefix="/passport",
    tags=["Passport"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PassportRead],
            summary="Get all Passport")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Passport

        - **skip**: int - The number of Passport
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Passport
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return passport_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PassportRead,
             summary="Create Passport")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PassportCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Passport

        - **document_number**: str
        - **date_of_issue**: datetime.date
        - **date_to**: datetime.date
        - **document_link**: str
        - **profile_id**: str
    """
    Authorize.jwt_required()
    return passport_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PassportRead,
            summary="Get Passport by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Passport by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return passport_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PassportRead,
            summary="Update Passport")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PassportUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Passport

        - **id**: UUID - the ID of Passport to update. This is required.
        - **document_link**: str (url)
    """
    Authorize.jwt_required()
    return passport_service.update(
        db,
        db_obj=passport_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Passport")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Passport

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    passport_service.remove(db, str(id))
