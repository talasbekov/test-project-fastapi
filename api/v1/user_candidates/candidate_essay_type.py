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
            summary="Get all Candidates")
async def get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):    
    """
        Get all Candidates.

        - **skip**: int - The number of badges to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of badges to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.get_multiple(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateEssayTypeRead,
            summary="Get a Candidate by id")
async def get_by_id(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID = None
):
    """
        Get a Candidate by id.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.get_by_id(db, id)


@router.post("", dependencies=[Depends(HTTPBearer())],
            summary="Create a Candidate",
            response_model=CandidateEssayTypeRead,
            )
async def create(
    db: Session = Depends(get_db),
    candidate_stage: CandidateEssayTypeCreate = None,
    Authorize: AuthJWT = Depends()
):
    """
        Create a Candidate.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.create(db, candidate_stage)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateEssayTypeRead,
            summary="Update a Candidate")
async def update(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID = None,
    candidate_stage: CandidateEssayTypeUpdate = None
):
    """
        Update a Candidate.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.update(db, id, candidate_stage)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
            response_description="Candidate deleted",
            summary="Delete a Candidate")
async def delete(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID = None
):
    """
        Delete a Candidate.
    """
    Authorize.jwt_required()
    return candidate_essay_type_service.remove(db, id)
