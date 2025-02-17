import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    CandidateStageAnswerCreate,
    CandidateStageAnswerRead,
    CandidateStageListAnswerCreate,
    CandidateStageAnswerUpdate,
)
from services import candidate_stage_answer_service

router = APIRouter(prefix="/candidate_stage_answer",
                   tags=["CandidateStageAnswer"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("",
            dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageAnswerRead],
            summary="Get all CandidateStageAnswer")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all CandidateStageAnswer.

        - **skip**: int - The number of CandidateStageAnswer
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateStageAnswer
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.get_multiple(db, skip, limit)


@router.get("/{id}",
            dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageAnswerRead,
            summary="Get a CandidateStageAnswer by id")
async def get_by_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: str = None
):
    """
        Get a CandidateStageAnswer by id.

        - **id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.get_by_id(db, str(id))


@router.get("/all/candidate/{candidate_id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Get all CandidateStageAnswer by candidate_id")
async def get_all_by_candidate_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        candidate_id: str = None
):
    """
        Get all CandidateStageAnswer by candidate_id.

        - **candidate_id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.get_all_by_candidate_id(
        db, str(candidate_id))


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             summary="Create a CandidateStageAnswer for single question",
             response_model=CandidateStageAnswerRead)
async def create(
        db: Session = Depends(get_db),
        body: CandidateStageAnswerCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a CandidateStageAnswer for single question

        - **candidate_stage_question_id**: UUID - required.
            Уникальный идентификатор для вопроса, на который дается ответ.
        - **type**: str - optional.
            Тип данных ответа, который может быть:
            String, Choice, Text, Document, Essay, Sport score, Dropdown
        - **answer_str**: str - optional.
            Фактический ответ, предоставленный кандидатом,
            если тип ответа - строка.
        - **answer_bool**: boolean - optional.
            Логическое значение, представляющее ответ,
            если тип ответа является логическим.
        - **answer**: str - optional.
            Фактический ответ, предоставленный кандидатом,
            если тип ответа TEXT.
        - **document_link**: str - optional.
            Ссылка на документ или ресурс, подтверждающий ответ,
            предоставленный кандидатом, если тип ответа Document.
        - **document_number**: str - optional.
            Уникальный идентификатор документа или ресурса,
            на который ссылается поле document_link.
        - **candidate_essay_type_id**: UUID - optional.
            Уникальный идентификатор для типа вопроса эссе,
            на который требуется ответить, если type Essay
        - **candidate_id**: UUID - required.
            Уникальный идентификатор кандидата,
            который предоставляет ответ.
        - **category_id**: UUID - optional.
            Уникальный идентификатор для категории dropdown вопроса,
            на который дается ответ.
        - **sport_score**: int - optional. Числовая оценка.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.create(db, body)


@router.post("/list", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             summary="Create CandidateStageAnswer for multiple questions",
             response_model=List[CandidateStageAnswerRead])
async def create_list(
        db: Session = Depends(get_db),
        body: CandidateStageListAnswerCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create CandidateStageAnswer for multiple questions

        - **candidate_stage_question_id**: UUID - required.
            Уникальный идентификатор для вопроса,
            на который дается ответ.
        - **type**: str - optional.
            Тип данных ответа, который может быть:
            String, Choice, Text, Document, Essay,
            Sport score, Dropdown
        - **answer_str**: str - optional.
            Фактический ответ, предоставленный кандидатом,
            если тип ответа - строка.
        - **answer_bool**: boolean - optional.
            Логическое значение, представляющее ответ,
            если тип ответа является логическим.
        - **answer**: str - optional.
            Фактический ответ,
            предоставленный кандидатом, если тип ответа TEXT.
        - **document_link**: str - optional.
            Ссылка на документ или ресурс,
            подтверждающий ответ, предоставленный кандидатом,
            если тип ответа Document.
        - **document_number**: str - optional.
            Уникальный идентификатор документа или ресурса,
            на который ссылается поле document_link.
        - **candidate_essay_type_id**: UUID - optional.
            Уникальный идентификатор для типа вопроса эссе,
            на который требуется ответить, если type Essay
        - **candidate_id**: UUID - required.
            Уникальный идентификатор кандидата,
            который предоставляет ответ.
        - **category_id**: UUID - optional.
            Уникальный идентификатор для категории dropdown вопроса,
            на который дается ответ.
        - **sport_score**: int - optional. Числовая оценка.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.create_list(db, body)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageAnswerRead,
            summary="Update a CandidateStageAnswer")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: str = None,
        body: CandidateStageAnswerUpdate = None
):
    """
        Update a CandidateStageAnswer.

        - **id**: required and should exist in the database.
        - **candidate_stage_question_id**: UUID - required.
            Уникальный идентификатор для вопроса,
            на который дается ответ.
        - **type**: str - optional.
            Тип данных ответа, который может быть:
            String, Choice, Text, Document,
            Essay, Sport score, Dropdown
        - **answer_str**: str - optional.
            Фактический ответ,
            предоставленный кандидатом,
            если тип ответа - строка.
        - **answer_bool**: boolean - optional.
            Логическое значение, представляющее ответ,
            если тип ответа является логическим.
        - **answer**: str - optional.
            Фактический ответ, предоставленный кандидатом,
            если тип ответа TEXT.
        - **document_link**: str - optional.
            Ссылка на документ или ресурс,
            подтверждающий ответ, предоставленный кандидатом,
            если тип ответа Document.
        - **document_number**: str - optional.
            Уникальный идентификатор документа или ресурса,
            на который ссылается поле document_link.
        - **candidate_essay_type_id**: UUID - optional.
            Уникальный идентификатор для типа вопроса эссе,
            на который требуется ответить, если type Essay
        - **candidate_id**: UUID - required.
            Уникальный идентификатор кандидата,
            который предоставляет ответ.
        - **category_id**: UUID - optional.
            Уникальный идентификатор для категории
            dropdown вопроса, на который дается ответ.
    """
    Authorize.jwt_required()
    return candidate_stage_answer_service.update(db,
                                                 db_obj=candidate_stage_answer_service.get_by_id(
                                                     db, id),
                                                 obj_in=body)


@router.delete("/{id}",
               dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a CandidateStageAnswer")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: str = None
):
    """
        Delete a CandidateStageAnswer.

        - **id**: required and should exist in the database.
    """
    Authorize.jwt_required()
    candidate_stage_answer_service.delete(db, str(id))
