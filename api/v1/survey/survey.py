import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import SurveyCreate, SurveyUpdate, SurveyRead
from services import survey_service

router = APIRouter(prefix="/surveys",
                   tags=["Surveys"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SurveyRead],
            summary="Get all Surveys")
async def get_all_active(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Surveys

        - **skip**: int - The number of surveys to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of surveys to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return survey_service.get_all_active(db, skip, limit)


@router.get("/archives", dependencies=[Depends(HTTPBearer())],
            response_model=List[SurveyRead],
            summary="Get all archive Surveys")
async def get_all_not_active(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all archive Surveys

        - **skip**: int - The number of surveys to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of surveys to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return survey_service.get_all_not_active(db, skip, limit)


@router.get("/drafts", dependencies=[Depends(HTTPBearer())],
            response_model=List[SurveyRead],
            summary="Get all draft Surveys")
async def get_all_draft(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all draft Surveys

        - **skip**: int - The number of surveys to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of surveys to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return survey_service.get_all_draft(db, skip, limit)


@router.get("/my", dependencies=[Depends(HTTPBearer())],
            response_model=List[SurveyRead],
            summary="Get all Surveys by jurisdiction")
async def get_by_jurisdiction(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Surveys by jurisdiction

        - **skip**: int - The number of surveys to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of surveys to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return survey_service.get_by_jurisdiction(db, role, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SurveyRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SurveyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new survey

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return survey_service.create(db, body)


@router.post("/draft", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SurveyRead,
             summary="Save as draft")
async def save_as_draft(*,
                 db: Session = Depends(get_db),
                 body: SurveyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new survey

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return survey_service.save_as_draft(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SurveyRead,
            summary="Get Survey by id")
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
    return survey_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SurveyRead,
            summary="Update Survey")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: SurveyUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update survey

        - **id**: UUID - the ID of survey to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return survey_service.update(db,
                                 db_obj=survey_service.get_by_id(db, id),
                                 obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Survey")
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
    survey_service.remove(db, id)
