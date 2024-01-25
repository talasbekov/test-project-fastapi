import pickle
import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List, Union, Dict, Any, Optional
from utils import get_access_token_by_user_id
from core import get_db
from models import LanguageEnum
from schemas import (HrDocumentInit,
                     HrDocumentRead,
                     HrDocumentSign,
                     HrDocumentUpdate,
                     DraftHrDocumentCreate,
                     UserRead,
                     HrDocumentInitEcp,
                     HrDocumentSignEcp,
                     HrDocumentSignEcpWithIds,
                     QrRead)
from services import hr_document_service
from services.autotags import auto_tags
from tasks import task_sign_document_with_certificate

router = APIRouter(
    prefix="/hr-documents",
    tags=["HrDocuments"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("/not-signed",
            response_model=List[HrDocumentRead],
            summary="Get all not signed HrDocuments")
async def get_not_signed(*,
                         db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends(),
                         parent_id: str = None,
                         filter: str = '',
                         skip: int = 0,
                         limit: int = 10,
                         ):
    """
        Get all not signed HrDocuments

        - **skip**: int - The number of HrDocuments to skip
            before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response.
            This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results.
            This parameter is optional and defaults to None
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_not_signed_documents(
        db, user_id, parent_id, filter.lstrip().rstrip(), skip, limit)


@router.get("/signed", response_model=List[HrDocumentRead],
            summary="Get all not signed HrDocuments")
async def get_signed(*,
                     db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(),
                     parent_id: str = None,
                     filter: str = '',
                     skip: int = 0,
                     limit: int = 10,
                     ):
    """
        Get all not signed HrDocuments

        - **skip**: int - The number of HrDocuments to skip
            before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response.
            This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results.
            This parameter is optional and defaults to None
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_signed_documents(
        db, user_id, parent_id, filter.lstrip().rstrip(), skip, limit)


@router.get("/initialized", response_model=List[HrDocumentRead],
            summary="Get all initialized HrDocuments")
async def get_initialized(*,
                          db: Session = Depends(get_db),
                          Authorize: AuthJWT = Depends(),
                          parent_id: Optional[str] = None,
                          filter: str = '',
                          skip: int = 0,
                          limit: int = 10,
                          ):
    """
        Get all initialized HrDocuments

        - **skip**: int - The number of HrDocuments to skip
            before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response.
            This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results.
            This parameter is optional and defaults to None

    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_initialized_documents(
        db, str(user_id), parent_id, filter.lstrip().rstrip(), skip, limit)


@router.get("/all/",
            response_model=List[HrDocumentRead],
            summary="Get all al HrDocuments by user")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  user_id: str = None,
                  filter: str = '',
                  skip: int = 0,
                  limit: int = 10,
                  ):
    """
        Get all all HrDocuments

        - **skip**: int - The number of HrDocuments to skip
            before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response.
            This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results.
            This parameter is optional and defaults to None
        - **user_id**: UUID - optional defaults to authorized user.
            User ID of the subject of the HrDocument.

    """
    Authorize.jwt_required()
    if not user_id:
        user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_all_documents(
        db, user_id, filter.lstrip().rstrip(), skip, limit)


@router.get("/allDocuments/",
            response_model=List[HrDocumentRead],
            summary="Get all al HrDocuments by user")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10,
                  ):
    """
        Get all HrDocuments

        - **skip**: int - The number of HrDocuments to skip
            before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocuments to return in the response.
            This parameter is optional and defaults to 10.
        - **filter**: str - The value which returns filtered results.
            This parameter is optional and defaults to None
        - **user_id**: UUID - optional defaults to authorized user.
            User ID of the subject of the HrDocument.

    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_all_documents_of_user(
        db, user_id, skip, limit)


@router.post("/ecp_sign_all/", status_code=status.HTTP_200_OK,
             summary="Sign HrDocument with ecp")
def sign_ecp_all(*,
                 db: Session = Depends(get_db),
                 body: HrDocumentSignEcpWithIds,
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
    access_token = get_access_token_by_user_id(Authorize, db, user_id)
    byte_body = pickle.dumps(body)
    task = task_sign_document_with_certificate.delay(byte_body,
                                              str(user_id),
                                              access_token)
    return task.id


@router.post("/ecp_sign/{id}/", status_code=status.HTTP_200_OK,
             summary="Sign HrDocument with ecp")
def sign_ecp(*,
             db: Session = Depends(get_db),
             id: str,
             body: HrDocumentSignEcp,
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
    access_token = get_access_token_by_user_id(Authorize, db, user_id)
    hr_document_service.sign_with_certificate(db,
                                              str(id),
                                              body,
                                              str(user_id),
                                              access_token,
                                              )

@router.post("/ecp_initialize",
             status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentRead,
             summary="Initialize HrDocument")
async def initialize_with_certificate(*,
                     db: Session = Depends(get_db),
                     body: HrDocumentInitEcp,
                     Authorize: AuthJWT = Depends()
                     ):
    """
        Initialize HrDocument

        The user must have a role that allows them to create HR documents.

        - **hr_document_template_id**: UUID - required.
            HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD).
            This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database.
            A list of user IDs to be assigned to the HrDocument.
        - **document_step_users_ids**: UUID - required and should exist in database.
            Dictionary of priority to user IDs to be assigned to the HrDocument.
        - **certificate_blob**: string - required.
            The certificate's string representation.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    access_token = get_access_token_by_user_id(Authorize, db, user_id)
    return await hr_document_service.initialize_with_certificate(db,
                                                                 body,
                                                                 str(user_id),
                                                                 str(role),
                                                                 access_token,
                                                                 Authorize)

@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentRead,
             summary="Initialize HrDocument")
async def initialize(*,
                     db: Session = Depends(get_db),
                     body: HrDocumentInit,
                     Authorize: AuthJWT = Depends()
                     ):
    """
        Initialize HrDocument

        The user must have a role that allows them to create HR documents.

        - **hr_document_template_id**: UUID - required.
            HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD).
            This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database.
            A list of user IDs to be assigned to the HrDocument.
        - **document_step_users_ids**: UUID - required and should exist in database.
            Dictionary of priority to user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return await hr_document_service.initialize(db, body, user_id, role)


@router.get("/drafts", response_model=List[HrDocumentRead],
            summary="Get all Draft HrDocuments")
async def get_draft_documents(*,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends(),
                              parent_id: str = None,
                              filter: str = '',
                              skip: int = 0,
                              limit: int = 10,

                              ):
    """
        Get all Draft HrDocuments
    - **filter**: str - The value which returns filtered results.
        This parameter is optional and defaults to None
    - **skip**: int - The number of HrDocuments to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of HrDocuments to return in the response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_draft_documents(
        db, user_id, parent_id, filter, skip, limit)


@router.post("/drafts",
             status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentRead,
             summary="Save HrDocument to Draft")
async def save_to_draft(*,
                        db: Session = Depends(get_db),
                        body: DraftHrDocumentCreate,
                        Authorize: AuthJWT = Depends()
                        ):
    """
        Save HrDocument

    The user must have a role that allows them to create HR documents.

        - **hr_document_template_id**: UUID - required.
            HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD).
            This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database.
            A list of user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.save_to_draft(db, user_id, body, role)


@router.post("/drafts/{id}",
             status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentRead,
             summary="Initialize Draft HrDocument")
async def initialize_draft_document(*,
                        db: Session = Depends(get_db),
                        body: DraftHrDocumentCreate,
                        Authorize: AuthJWT = Depends(),
                        id: str
):
    """
        Initialize Draft HrDocument

        The user must have a role that allows them to create HR documents.

        - **document_id**: UUID - required.
        - **due_date**: the end date of this document - format (YYYY-MM-DD).
            This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database.
            A list of user IDs to be assigned to the HrDocument.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.initialize_draft_document(
        db, body, id, user_id, role)


@router.put("/{id}/", response_model=HrDocumentRead,
            summary="Update HrDocument")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: HrDocumentUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update HrDocument

        - **id**: UUID - the id of HrDocument. This is required.
        - **hr_document_template_id**: UUID - required.
            HrDocument will be initialized based on HrDocumentTemplate.
        - **due_date**: the end date of this document - format (YYYY-MM-DD).
            This parameter is required.
        - **properties**: A dictionary containing properties for the HrDocument.
        - **user_ids**: UUID - required and should exist in database.
            A list of user IDs to be assigned to the HrDocument.
        - **status**: the status of the HrDocument.
            This field should accept one of the following statuses:

        * Иницилизирован
        * В процессе
        * Завершен
        * Отменен
        * На доработке
    """
    Authorize.jwt_required()
    return hr_document_service.update_document(
        db=db,
        hr_document=hr_document_service.get_by_id(db, str(id)),
        hr_document_update=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete HrDocument")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete HrDocument

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    hr_document_service.remove(db, str(id))


@router.post("/{id}/", status_code=status.HTTP_200_OK,
             summary="Sign HrDocument")
def sign(*,
               db: Session = Depends(get_db),
               id: str,
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
    hr_document_service.sign(db, str(id), body, user_id)


@router.get("/{id}/", response_model=HrDocumentRead,
            summary="Get HrDocument by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get HrDocument by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_document_service.get_by_id_for_api(db, str(id))


@router.get('/generate/{id}/', status_code=status.HTTP_200_OK,
            summary="Generate HrDocument")
async def generate(*,
                   db: Session = Depends(get_db),
                   id: str,
                   Authorize: AuthJWT = Depends()
                   ):
    """
        This endpoint generates a HR document based on the given document ID. (pdf)

        It takes a document ID as input,
        retrieves the corresponding HR document from the database,
        retrieves the HR document template associated with the document,
        renders the template with the document's properties,
        and saves the resulting Word document to a temporary file.
        It then returns a FileResponse
        containing the generated document as an attachment
        that can be downloaded by the user.

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return await hr_document_service.generate(db, str(id), LanguageEnum.kz)


@router.get('/generate-html/{id}/', status_code=status.HTTP_200_OK,
            summary="Generate HrDocument")
async def generate_html(*,
                        db: Session = Depends(get_db),
                        id: str,
                        Authorize: AuthJWT = Depends()
                        ):
    """
        This endpoint generates a HR document based on the given document ID. (html)

        It takes a document ID as input,
        retrieves the corresponding HR document from the database,
        retrieves the HR document template associated with the document,
        renders the template with the document's properties,
        and saves the resulting Word document to a temporary file.
        It then returns a FileResponse containing
        the generated document as an attachment that can be downloaded by the user.

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return await hr_document_service.generate_html(db, str(id), LanguageEnum.kz)


@router.get('/options', status_code=status.HTTP_200_OK,
            summary="Get data by option")
async def get_data_by_option(*,
                             db: Session = Depends(get_db),
                             option: str,
                             data_taken: Optional[str] = None,
                             id: Optional[str] = None,
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
    res = hr_document_service.get_all_by_option(
        db, option, data_taken, id, type, skip, limit)
    return res


@router.get('/signee/{id}/', response_model=UserRead)
async def get_signee(*,
                     db: Session = Depends(get_db),
                     id: str,
                     Authorize: AuthJWT = Depends()
                     ):
    """
        Get signee

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hr_document_service.get_signee(db, str(id))


@router.post('/initialize/staff_list/{id}/', response_model=HrDocumentRead,
             summary="Initialize HrDocument from staff list")
async def initialize_from_staff_list(*,
                                     db: Session = Depends(get_db),
                                     id: str,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
        Initialize HrDocument from staff list

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return await hr_document_service.initialize_super_document(db=db,
                                                               staff_list_id=id,
                                                               user_id=user_id,
                                                               role=role)
    
@router.get('/qrs/{id}/', response_model=List[QrRead])
async def get_qrs(*,
                     db: Session = Depends(get_db),
                     id: str,
                     Authorize: AuthJWT = Depends()
                     ):
    """
        Get qrs

        - **id**: hr_document_id - required.
    """
    Authorize.jwt_required()
    return hr_document_service.generate_qrs(db, id)

@router.get('/generate_draft_for_expiring/')
async def generate_draft_for_expiring(*,
                                      contract_id: str,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends()
                                      ):
    """
        Generate draft for expiring contracts

    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    properties = {}
    required_properties = ["contract", "father", "name", "officer", "position", "rank", "surname"]
    for prop in required_properties:
        properties[prop] = auto_tags.get(prop).handle(db, str(user_id))
    role = Authorize.get_raw_jwt()['role']
    return await hr_document_service.generate_document_for_expiring(db, contract_id, role, properties)