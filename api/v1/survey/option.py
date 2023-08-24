import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import OptionCreate, OptionUpdate, OptionRead, OptionReadPagination
from services import option_service

router = APIRouter(prefix="/options",
                   tags=["Options"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=OptionReadPagination,
            summary="Get all Options")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Option

        - **skip**: int - The number of options to skip before returning the results. 
                This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of options to return in the response. 
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return {
        'total': option_service.get_count(db),
        'objects': option_service.get_multi(db, skip, limit)
    }


@router.get("/question-id/", dependencies=[Depends(HTTPBearer())],
            response_model=List[OptionRead],
            summary="Get all Options by question id")
async def get_by_question(*,
                          db: Session = Depends(get_db),
                          question_id: str,
                          Authorize: AuthJWT = Depends()
                          ):
    """
        Get all Option by question id

    """
    Authorize.jwt_required()
    return option_service.get_by_question(db, question_id)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=List[OptionRead],
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: List[OptionCreate],
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new question

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return option_service.create_list(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=OptionRead,
            summary="Get Option by id")
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
    return option_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=OptionRead,
            summary="Update Option")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: OptionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update question

        - **id**: UUID - the ID of question to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return option_service.update(db,
                                 db_obj=option_service.get_by_id(db, str(id)),
                                 obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Option")
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
    option_service.remove(db, str(id))
