import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import CandidateRead, CandidateCreate, CandidateUpdate, CandidateEssayUpdate
from services import candidate_service

router = APIRouter(prefix="/candidates", tags=["Candidates"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateRead],
            summary="Get all Candidate")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all Candidates.

        - **skip**: int - The number of Candidate to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Candidate to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_service.get_multiple(db, skip, limit)


@router.get("/drafts", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateRead],
            summary="Get all Draft Candidate")
async def get_all_draft_candidates(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all Draft Candidates.

        - **skip**: int - The number of Candidate to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Candidate to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_service.get_draft_candidates(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateRead,
            summary="Get a Candidate by id")
async def get_by_id(
        db: Session = Depends(get_db),
        id: uuid.UUID = None,
        Authorize: AuthJWT = Depends()
):
    """
        Get a Candidate by id.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_service.get_by_id(db, id)


@router.post("", dependencies=[Depends(HTTPBearer())],
             summary="Create a Candidate",
             response_model=CandidateRead)
async def create(
        body: CandidateCreate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()
):
    """
        Create a Candidate.

        - **staff_unit_curator_id**: UUID - required and should exist in the database. This is a staff unit who is the supervisor of a certain candidate
        - **staff_unit_id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_service.create(db, body)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateRead,
            summary="Update a Candidate")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        body: CandidateUpdate = None
):
    """
        Update a Candidate.

        - **staff_unit_curator_id**: UUID - optional and should exist in the database. This is a staff unit who is the supervisor of a certain candidate
        - **staff_unit_id**: UUID - optional and should exist in the database.
        - **status**: str - optional. Available statuses are provided below:

        1. Активный
        2. Черновик
    """
    Authorize.jwt_required()
    return candidate_service.update(db, id, body)


@router.patch("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateRead,
            summary="Update Essay for Candidate")
async def update_essay(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        body: CandidateEssayUpdate = None
):
    """
        Update a Candidate.

        - **id**: UUID - required and should exist in the database.
        - **essay_id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_service.update_essay(db=db, id=id, essay_id=body.essay_id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete a Candidate")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Delete a Candidate.

        - **id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    candidate_service.remove(db, id)
