import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import (
    CandidateEssayTypeCreate,
    CandidateEssayTypeRead,
    CandidateEssayTypeUpdate,
    CandidateEssayTypeSetToCandidate
)
from services import candidate_essay_type_service

router = APIRouter(
    prefix="/candidate_essay_type",
    tags=["CandidateEssayType"],
    dependencies=[
        Depends(
            HTTPBearer())])


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

        - **skip**: int - The number of CandidateEssayType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateEssayType
            to return in the response.
            This parameter is optional and defaults to 100.
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


@router.post("/candidate/{candidate_id}", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             summary="Create a CandidateEssayType and set to Candidate",
             response_model=CandidateEssayTypeRead)
async def create_and_set_to_candidate(
        db: Session = Depends(get_db),
        candidate_id: uuid.UUID = None,
        body: CandidateEssayTypeSetToCandidate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a CandidateEssayType and set to Candidate.

        - **id**: UUID - optional and should exist in the database.
        - **name**: str - optional

        1. If candidate chooses from existing essay types then you can set id of essay
        2. If candidate creates a new essay you can send name of the new essay to create
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.set_to_candidate(
        db, body, candidate_id)


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
                                               db_obj=candidate_essay_type_service.get_by_id(
                                                   db, id),
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
