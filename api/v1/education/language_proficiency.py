import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (LanguageProficiencyCreate,
                               LanguageProficiencyRead,
                               LanguageProficiencyUpdate)
from services.education import language_proficiency_service

router = APIRouter(prefix="/language_proficiencies",
                   tags=["LanguageProficiencies"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[LanguageProficiencyRead],
            summary="Get all LanguageProficiencies")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all LanguageProficiencies

    - **skip**: int - The number of LanguageProficiencies
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of LanguageProficiencies
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return language_proficiency_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=LanguageProficiencyRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: LanguageProficiencyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new LanguageProficiency

        - **name**: required
    """
    Authorize.jwt_required()
    return language_proficiency_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LanguageProficiencyRead,
            summary="Get LanguageProficiency by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get LanguageProficiency by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return language_proficiency_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LanguageProficiencyRead,
            summary="Update LanguageProficiency")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: LanguageProficiencyUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update LanguageProficiency

        - **id**: UUID - the ID of LanguageProficiency to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return language_proficiency_service.update(
        db,
        db_obj=language_proficiency_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete LanguageProficiency")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete LanguageProficiency

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    language_proficiency_service.remove(db, str(id))
