import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT 
from sqlalchemy.orm import Session
from typing import List 

from core import get_db
from schemas import (
    CandidateStageAnswerCreate,
    CandidateStageAnswerRead,
    CandidateStageAnswerIdRead,
    CandidateStageListAnswerCreate,
    CandidateStageAnswerUpdate,
)
from services import candidate_stage_answer_service


router = APIRouter(prefix="/candidate_stage_answer", tags=["CandidateStageAnswer"], dependencies=[Depends(HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageAnswerRead],
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
    return candidate_stage_answer_service.get_multiple(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageAnswerRead,
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
    return candidate_stage_answer_service.get_by_id(db, id)


@router.post("", dependencies=[Depends(HTTPBearer())],
            summary="Create a Candidate",
            response_model=CandidateStageAnswerIdRead,
            )
async def create(
    db: Session = Depends(get_db),
    candidate_stage: CandidateStageAnswerCreate = None,
    Authorize: AuthJWT = Depends()
):
    """
        Create a Answer for Question.

        - **candidate_stage_question_id**: UUID - required. Уникальный идентификатор для вопроса, на который дается ответ.
        - **type**: str - optional. Тип данных ответа, который может быть String, Choice, Text, Document, Essay, Sport score, Dropdown
        - **answer_str**: str - optional. Фактический ответ, предоставленный кандидатом, если тип ответа - строка.
        - **answer_bool**: boolean - optional. Логическое значение, представляющее ответ, если тип ответа является логическим.
        - **answer**: str - optional. Фактический ответ, предоставленный кандидатом, если тип ответа TEXT.
        - **document_link**: str - optional. Ссылка на документ или ресурс, подтверждающий ответ, предоставленный кандидатом, если тип ответа Document.
        - **document_number**: str - optional. Уникальный идентификатор документа или ресурса, на который ссылается поле document_link.
        - **candidate_essay_type_id**: UUID - optional. Уникальный идентификатор для типа вопроса эссе, на который требуется ответить, если type Essay
        - **candidate_id**: UUID - required. Уникальный идентификатор кандидата, который предоставляет ответ.
        - **category_id**: UUID - optional. Уникальный идентификатор для категории dropdown вопроса, на который дается ответ.
        - **sport_score**: int - optional. Числовая оценка.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.create(db, candidate_stage)


@router.post("/list", dependencies=[Depends(HTTPBearer())],
            summary="Create a list of answers",
            )
async def create_list(
    db: Session = Depends(get_db),
    candidate_stage: CandidateStageListAnswerCreate = None,
    Authorize: AuthJWT = Depends()
):
    """
        Create a Candidate.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.create_list(db, candidate_stage)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageAnswerRead,
            summary="Update a Candidate")
async def update(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID = None,
    candidate_stage: CandidateStageAnswerUpdate = None
):
    """
        Update a Candidate.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.update(db, id, candidate_stage)


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
    return candidate_stage_answer_service.delete(db, id)
