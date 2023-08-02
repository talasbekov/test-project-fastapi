import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (DocumentStaffFunctionAdd, DocumentStaffFunctionRead,
                     DocumentStaffFunctionUpdate, DocumentStaffFunctionConstructorAdd,
                     DocumentStaffFunctionAppendToStaffUnit)
from services import document_staff_function_service

router = APIRouter(
    prefix="/document_staff_function",
    tags=["DocumentStaffFunction"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DocumentStaffFunctionRead],
            summary="Get all DocumentStaffFunction")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all DocumentStaffFunction

    - **skip**: int - The number of DocumentStaffFunction
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of DocumentStaffFunction
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return document_staff_function_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionRead,
            summary="Get DocumentStaffFunction by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get DocumentStaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return document_staff_function_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionRead,
            summary="Update DocumentStaffFunction")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: DocumentStaffFunctionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update DocumentStaffFunction

    """
    Authorize.jwt_required()
    return document_staff_function_service.update(
        db,
        db_obj=document_staff_function_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete DocumentStaffFunction")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete DocumentStaffFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    document_staff_function_service.remove(db, str(id))


@router.post('/duplicate/{id}/', status_code=status.HTTP_201_CREATED,
             response_model=DocumentStaffFunctionRead)
def duplicate(*,
              db: Session = Depends(get_db),
              id: uuid.UUID,
              Authorize: AuthJWT = Depends()
              ):
    Authorize.jwt_required()
    return document_staff_function_service.duplicate(db, str(id))


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=DocumentStaffFunctionRead)
async def create_function(*,
                          db: Session = Depends(get_db),
                          body: DocumentStaffFunctionAdd,
                          Authorize: AuthJWT = Depends()
                          ):
    Authorize.jwt_required()
    return document_staff_function_service.create_function(db, body)


@router.post("/constructor/", status_code=status.HTTP_201_CREATED,
             response_model=DocumentStaffFunctionRead)
async def create_function_for_constructor(*,
                                          db: Session = Depends(get_db),
                                          body: DocumentStaffFunctionConstructorAdd,
                                          Authorize: AuthJWT = Depends()
                                          ):
    Authorize.jwt_required()
    return document_staff_function_service.create_function_for_constructor(
        db, body)


@router.get('/staff_unit/{id}')
async def get_staff_units_by_id(*,
                                db: Session = Depends(get_db),
                                id: uuid.UUID,
                                Authorize: AuthJWT = Depends()
                                ):
    Authorize.jwt_required()
    return document_staff_function_service.get_staff_units_by_id(db, str(id))


@router.post('/append_to_staff_unit/', status_code=status.HTTP_201_CREATED)
async def append_to_staff_unit(*,
                               db: Session = Depends(get_db),
                               body: DocumentStaffFunctionAppendToStaffUnit,
                               Authorize: AuthJWT = Depends()
                               ):
    Authorize.jwt_required()
    return document_staff_function_service.append_to_staff_unit(db, body)
