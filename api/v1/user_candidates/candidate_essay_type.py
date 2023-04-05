import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import CandidateEssayTypeCreate, CandidateEssayTypeRead, CandidateEssayTypeUpdate
from services import candidate_essay_type_service

router = APIRouter(prefix="/candidate_essay_type", tags=["CandidateEssayType"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateEssayTypeRead],
            summary="Get all CandidateEssayType")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all CandidateEssayType.

        - **skip**: int - The number of CandidateEssayType to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateEssayType to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.get_multi(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateEssayTypeRead,
            summary="Get a CandidateEssayType by id")
async def get_by_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Get a CandidateEssayType by id.

        - **id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.get_by_id(db, id)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             summary="Create a CandidateEssayType",
             response_model=CandidateEssayTypeRead)
async def create(
        db: Session = Depends(get_db),
        body: CandidateEssayTypeCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a CandidateEssayType.

        - **name**: str - required
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.create(db, body)


@router.put("/{id}", status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(HTTPBearer())],
            response_model=CandidateEssayTypeRead,
            summary="Update a CandidateEssayType")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        body: CandidateEssayTypeUpdate = None
):
    """
        Update a CandidateEssayType.

        - **id**: required and should exist in the database.
        - **name**: str - required
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.update(db,
                                               db_obj=candidate_essay_type_service.get_by_id(db, id),
                                               obj_in=body)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete a CandidateEssayType")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Delete a CandidateEssayType.

        - **id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    candidate_essay_type_service.remove(db, id)
