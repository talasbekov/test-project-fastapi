
import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ArchiveDocumentStaffFunctionRead,
                     ArchiveDocumentStaffFunctionUpdate)

from services import document_archive_staff_function_service


router = APIRouter(prefix="/archive_document_staff_function",
                   tags=["ArchiveDocumentStaffFunction"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ArchiveDocumentStaffFunctionRead],
            summary="Get all ArchiveDocumentStaffFunction")
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
    return document_archive_staff_function_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveDocumentStaffFunctionRead,
            summary="Get ArchiveDocumentStaffFunction by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get DocumentStaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return document_archive_staff_function_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveDocumentStaffFunctionRead,
            summary="Update ArchiveDocumentStaffFunction")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ArchiveDocumentStaffFunctionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update DocumentStaffFunction

    """
    Authorize.jwt_required()
    return document_archive_staff_function_service.update(
        db,
        db_obj=document_archive_staff_function_service.get_by_id(db, str(id)),
        obj_in=body)
