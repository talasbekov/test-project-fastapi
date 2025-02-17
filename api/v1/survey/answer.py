import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (AnswerCreate, AnswerUpdate, AnswerRead,
                     AnswerReadPagination)
from services import answer_service

router = APIRouter(prefix="/answers",
                   tags=["Answers"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=AnswerReadPagination,
            summary="Get all Answers")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Answer

        - **skip**: int - The number of answers to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of answers to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return {
        'total': answer_service.get_count(db),
        'objects': answer_service.get_multi(db, skip, limit)
    }


@router.get("/survey/{survey_id}", dependencies=[Depends(HTTPBearer())],
            response_model=List[AnswerRead],
            summary="Get all by survey")
async def get_by_survey_id(*,
                  db: Session = Depends(get_db),
                  survey_id: uuid.UUID,
                  user_id: uuid.UUID = None,
                  Authorize: AuthJWT = Depends()):
    """
        Get all Answer by survey

        - **skip**: int - The number of answers to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of answers to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return answer_service.get_by_survey_id(db, str(survey_id), str(user_id))


@router.get("/survey/{survey_id}/users", dependencies=[Depends(HTTPBearer())],
            summary="Get responded users")
async def get_responded_users(*,
                  db: Session = Depends(get_db),
                  survey_id: uuid.UUID,
                  Authorize: AuthJWT = Depends()):
    """
        Get responded users
    """
    Authorize.jwt_required()
    return answer_service.get_responded_users(db, str(survey_id))


@router.get("/survey/{survey_id}/statistics", dependencies=[Depends(HTTPBearer())],
            summary="Get all by survey")
async def analyze_by_staff_division(*,
                  survey_id: uuid.UUID,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Answer by survey

        - **skip**: int - The number of answers to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of answers to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return answer_service.analyze_by_staff_division(str(survey_id))


@router.get("/survey/{survey_id}/questions", dependencies=[Depends(HTTPBearer())],
            summary="Get all by question")
async def analyze_by_questions(*,
                survey_id: uuid.UUID,
                db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()
                ):
    """
        Get all Answer by question

        - **skip**: int - The number of answers to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of answers to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return answer_service.analyze_by_question(db, str(survey_id))


@router.get("/question-text/{question_id}/", dependencies=[Depends(HTTPBearer())],
            summary="Analyze question with text type")
async def analyze_by_questions(*,
                question_id: uuid.UUID,
                db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()
                ):
    """
        Get all Answer by question

        - **skip**: int - The number of answers to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of answers to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return answer_service.analyze_by_question_with_text_type(db, str(question_id))



@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=List[AnswerRead],
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: List[AnswerCreate],
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new question

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return answer_service.create_list(db, body, user_id)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AnswerRead,
            summary="Get Answer by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get question by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return answer_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AnswerRead,
            summary="Update Answer")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: AnswerUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update question

        - **id**: UUID - the ID of question to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return answer_service.update(db,
                                 db_obj=answer_service.get_by_id(db, str(id)),
                                 obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Answer")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete question

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    answer_service.remove(db, str(id))
