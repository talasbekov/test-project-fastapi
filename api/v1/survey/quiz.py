import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import QuizCreate, QuizUpdate, QuizRead
from services import quiz_service

router = APIRouter(prefix="/quizzes",
                   tags=["Quizzess"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuizRead],
            summary="Get all Quizzes")
async def get_all_active(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Quizzes

        - **skip**: int - The number of quizzes to skip before returning the results.
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of quizzes to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return quiz_service.get_all_active(db, skip, limit)


@router.get("/archives", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuizRead],
            summary="Get all archive Quizzes")
async def get_all_not_active(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all archive Quizzes

        - **skip**: int - The number of quizzes to skip before returning the results.
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of quizzes to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return quiz_service.get_all_not_active(db, skip, limit)


@router.get("/drafts", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuizRead],
            summary="Get all draft Quizzes")
async def get_all_draft(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all draft Quizzes

        - **skip**: int - The number of quizzes to skip before returning the results.
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of quizzes to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return quiz_service.get_all_draft(db, skip, limit)


@router.get("/my", dependencies=[Depends(HTTPBearer())],
            response_model=List[QuizRead],
            summary="Get all Quizzes by jurisdiction")
async def get_by_jurisdiction(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Quizzes by jurisdiction

        - **skip**: int - The number of quizzes to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of quizzes to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return quiz_service.get_by_jurisdiction(db, role, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=QuizRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: QuizCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new survey

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return quiz_service.create(db, body)


@router.post("/draft", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=QuizRead,
             summary="Save as draft")
async def save_as_draft(*,
                 db: Session = Depends(get_db),
                 body: QuizCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new survey

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return quiz_service.save_as_draft(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=QuizRead,
            summary="Get Quiz by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get survey by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return quiz_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=QuizRead,
            summary="Update Quiz")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: QuizUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update survey

        - **id**: UUID - the ID of survey to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return quiz_service.update(db,
                                 db_obj=quiz_service.get_by_id(db, id),
                                 obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Quiz")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete survey

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    quiz_service.remove(db, id)
