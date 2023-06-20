import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import QuestionCreate, QuestionUpdate, QuestionRead
from services import question_service

router = APIRouter(prefix="/questions",
                   tags=["Questions"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuestionRead],
            summary="Get all Questions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Question

        - **skip**: int - The number of questions to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of questions to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return question_service.get_multi(db, skip, limit)


@router.get("/survey-id/", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuestionRead],
            summary="Get all Questions by survey id")
async def get_by_survey(*,
                  db: Session = Depends(get_db),
                  survey_id: uuid.UUID,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Question by survey

        - **skip**: int - The number of questions to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of questions to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return question_service.get_by_survey(db, survey_id)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=QuestionRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: QuestionCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new question

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return question_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=QuestionRead,
            summary="Get Question by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get question by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return question_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=QuestionRead,
            summary="Update Question")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: QuestionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update question

        - **id**: UUID - the ID of question to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return question_service.update(db,
                                   db_obj=question_service.get_by_id(db, id),
                                   obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Question")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete question

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    question_service.remove(db, id)
