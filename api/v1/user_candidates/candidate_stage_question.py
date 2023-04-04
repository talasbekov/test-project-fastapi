import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import CandidateStageQuestionCreate, CandidateStageQuestionRead
from services import candidate_stage_question_service

router = APIRouter(prefix="/candidate_stage_question", tags=["CandidateStageQuestion"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageQuestionRead],
            summary="Get all CandidateStageQuestion")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all CandidateStageQuestion.

        - **skip**: int - The number of CandidateStageQuestion to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateStageQuestion to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_stage_question_service.get_multiple(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageQuestionRead,
            summary="Get a CandidateStageQuestion by id")
async def get_by_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Get a CandidateStageQuestion by id.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_question_service.get_by_id(db, id)


@router.post("", dependencies=[Depends(HTTPBearer())],
             status_code=status.HTTP_201_CREATED,
             summary="Create a CandidateStageQuestion",
             response_model=CandidateStageQuestionRead,
             )
async def create(
        db: Session = Depends(get_db),
        candidate_stage: CandidateStageQuestionCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a Candidate.

        - **question**: str - required
        - **question_type**: str - required
    """
    Authorize.jwt_required()
    return candidate_stage_question_service.create(db, candidate_stage)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageQuestionRead,
            summary="Update a CandidateStageQuestion")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        candidate_stage: CandidateStageQuestionRead = None
):
    """
        Update a CandidateStageQuestion.

        - **id**: UUID - required and should exist in the database.
        - **question**: str - required
        - **question_type**: str - required
    """
    Authorize.jwt_required()
    return candidate_stage_question_service.update(db, id, candidate_stage)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a CandidateStageQuestion")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Delete a CandidateStageQuestion.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_question_service.remove(db, id)
