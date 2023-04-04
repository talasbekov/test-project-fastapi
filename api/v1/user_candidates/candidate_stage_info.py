import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List 

from core import get_db
from schemas import CandidateStageInfoCreate, CandidateStageInfoRead, CandidateStageInfoUpdate
from services import candidate_stage_info_service


router = APIRouter(prefix="/candidate_stage_info", tags=["CandidateStageInfo"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageInfoRead],
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
    return candidate_stage_info_service.get_multiple(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageInfoRead,
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
    return candidate_stage_info_service.get_by_id(db, id)


@router.get("/all/{staff_unit_id}", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageInfoRead],
            summary="Get all Candidates by staff_unit_id")
async def get_all_by_staff_unit_id(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    staff_unit_id: uuid.UUID = None
):
    """
        Get all Candidates by staff_unit_id.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.get_all_by_staff_unit_id(db, staff_unit_id)


@router.get("/all/candidate/{candidate_id}", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageInfoRead],
            summary="Get all Candidates by candidate_id")
async def get_all_by_candidate_id(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    candidate_id: uuid.UUID = None
):
    """
        Get all Candidates by candidate_id.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.get_all_by_candidate_id(db, candidate_id)


@router.post("", dependencies=[Depends(HTTPBearer())],
            summary="Create a Candidate",
            response_model=CandidateStageInfoRead
            )
async def create(
    db: Session = Depends(get_db),
    candidate_stage: CandidateStageInfoCreate = None,
    Authorize: AuthJWT = Depends()
):
    """
        Create a Candidate.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.create(db, candidate_stage)


@router.patch("/{id}/sign", dependencies=[Depends(HTTPBearer())],
            summary="Sign a CandidateStageInfo",
            status_code=status.HTTP_202_ACCEPTED,
            response_model=CandidateStageInfoRead
)
async def sign_candidate(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
):
    """
        Sign a CandidateStageInfo

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.sign_candidate(db, id)


@router.patch("/{id}/reject", dependencies=[Depends(HTTPBearer())],
              summary="Sign a CandidateStageInfo",
              status_code=status.HTTP_202_ACCEPTED,
              response_model=CandidateStageInfoRead
)
async def reject_candidate(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
):
    """
        Reject a CandidateStageInfo

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.reject_candidate(db, id)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageInfoRead,
            summary="Update a Candidate")
async def update(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID = None,
    candidate_stage: CandidateStageInfoUpdate = None
):
    """
        Update a Candidate.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.update(db, id, candidate_stage)


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
    return candidate_stage_info_service.remove(db, id)
