import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HrDocumentInit, HrDocumentRead,
                     HrDocumentSign, HrDocumentUpdate, DraftHrDocumentCreate, DraftHrDocumentInit)
from services import hr_document_service

router = APIRouter(prefix="/hr-documents", tags=["HrDocuments"], dependencies=[Depends(HTTPBearer())])


@router.get("/not-signed", response_model=List[HrDocumentRead],
            summary="Get all not signed HrDocuments")
async def get_not_signed(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = None,
    skip: int = 0,
    limit: int = 10,
):
    """
        Get all not signed HrDocuments

        - **skip**: int - The number of HrDocuments to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response. This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results. This parameter is optional and defaults to None
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_not_signed_documents(db, user_id, filter, skip, limit)


@router.get("/initialized", response_model=List[HrDocumentRead],
            summary="Get all initialized HrDocuments")
async def get_initialized(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = None,
    skip: int = 0,
    limit: int = 10,
):
    """
        Get all initialized HrDocuments

        - **skip**: int - The number of HrDocuments to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response. This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results. This parameter is optional and defaults to None

    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_initialized_documents(db, user_id, filter, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=HrDocumentRead,
             summary="Initialize HrDocument")
async def initialize(*,
    db: Session = Depends(get_db),
    body: HrDocumentInit,
    Authorize: AuthJWT = Depends()
):
    """
        Initialize HrDocument

        The user must have a role that allows them to create HR documents.

        - **hr_document_template_id**: UUID - required. HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD). This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database. A list of user IDs to be assigned to the HrDocument.
        - **document_step_users_ids**: UUID - required and should exist in database. Dictionary of priority to user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.initialize(db, body, user_id, role)


@router.get("/drafts", response_model=List[HrDocumentRead],
            summary="Get all Draft HrDocuments")
async def get_draft_documents(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all Draft HrDocuments

        - **skip**: int - The number of HrDocuments to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_draft_documents(db, user_id, skip, limit)


@router.post("/drafts", status_code=status.HTTP_201_CREATED, response_model=HrDocumentRead,
             summary="Save HrDocument to Draft")
async def save_to_draft(*,
    db: Session = Depends(get_db),
    body: DraftHrDocumentCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Save HrDocument

        The user must have a role that allows them to create HR documents.

        - **hr_document_template_id**: UUID - required. HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD). This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database. A list of user IDs to be assigned to the HrDocument.
        - **document_step_users_ids**: UUID - required and should exist in database. Dictionary of priority to user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.save_to_draft(db, user_id, body, role)


@router.post("/drafts/{id}", status_code=status.HTTP_201_CREATED, response_model=HrDocumentRead,
             summary="Initialize Draft HrDocument")
async def initialize_draft_document(*,
    db: Session = Depends(get_db),
    body: DraftHrDocumentInit,
    Authorize: AuthJWT = Depends(),
    id: uuid.UUID
):
    """
        Initialize Draft HrDocument

        The user must have a role that allows them to create HR documents.

        - **document_id**: UUID - required.
        - **document_step_users_ids**: UUID - required and should exist in database. Dictionary of priority to user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.initialize_draft_document(db, body, id, user_id, role)


@router.put("/{id}/", response_model=HrDocumentRead,
            summary="Update HrDocument")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HrDocument

        - **id**: UUID - the id of HrDocument. This is required.
        - **hr_document_template_id**: UUID - required. HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD). This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **status**: the status of the HrDocument. This field should accept one of the following statuses:

        * Иницилизирован
        * В процессе
        * Завершен
        * Отменен
        * На доработке
    """
    Authorize.jwt_required()
    return hr_document_service.update(
        db=db,
        db_obj=hr_document_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete HrDocument")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete HrDocument

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    hr_document_service.remove(db, id)


@router.post("/{id}/", status_code=status.HTTP_200_OK,
             summary="Sign HrDocument")
async def sign(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentSign,
    Authorize: AuthJWT = Depends()
):
    """
        Sign HrDocument

        The user must have a role that allows them to sign this HR document.

        - **id**: UUID - the ID of HrDocument. This is required.
        - **comment**: A comment on the signed document.
        - **is_signed**: bool - indicating whether the document is signed.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    hr_document_service.sign(db, id, body, user_id, role)


@router.get("/{id}/", response_model=HrDocumentRead,
            summary="Get HrDocument by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrDocument by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_document_service.get_by_id(db, id)


@router.get('/generate/{id}/', status_code=status.HTTP_200_OK,
            summary="Generate HrDocument")
async def generate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        This endpoint generates a HR document based on the given document ID.

        It takes a document ID as input, retrieves the corresponding HR document from the database, retrieves the HR document template associated with the document, renders the template with the document's properties, and saves the resulting Word document to a temporary file. It then returns a FileResponse containing the generated document as an attachment that can be downloaded by the user.

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hr_document_service.generate(db, id)


@router.get('/options', status_code=status.HTTP_200_OK,
            summary="Get data by option")
async def get_data_by_option(*,
    db: Session = Depends(get_db),
    option: str,
    data_taken: Optional[str] = None,
    id: Optional[uuid.UUID] = None,
    type: str = "write",
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends()
):
    """
        Get data by option

        - **option**: required. This field should accept one of the following options:

        * staff_unit
        * actual_staff_unit
        * staff_division
        * rank
        * badges
    """
    Authorize.jwt_required()
    res = hr_document_service.get_all_by_option(db, option, data_taken, id, type, skip, limit)
    return res
