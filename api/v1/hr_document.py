import pickle
import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List, Union, Dict, Any, Optional
from utils import get_access_token_by_user_id
from core import get_db
from models import LanguageEnum, ContractType, ActionType
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
from services import hr_document_service, hr_document_template_service
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

@router.get('/generate_document_for_expiring/{contract_id}/{contract_type_id}/', summary="Generate draft for expiring contracts")
async def generate_document_for_expiring(*,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends(),
                                      contract_id: str = None,
                                      contract_type_id: str = None,
                                      ):
    """
        Generate draft for expiring contracts

    """
    
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    properties = {}
    contract = db.query(ContractType).filter(ContractType.id == contract_type_id).all()[0]
    contract_new = {}
    # contract_new['name'] = contract.name
    contract_new['nameKZ'] = contract.nameKZ
    contract_new['value'] = contract.id
    contract_new['auto'] = False
    properties["contract"] = contract_new
    years = contract.years
    # properties["contract"] = await auto_tags.get("contract").handle(db, str(contract_id))
    template_id = hr_document_template_service.get_document_id_by_action_name(db, ActionType.RENEW_CONTRACT.value)
    required_properties = hr_document_template_service.extract_properties_by_template_id(db, template_id)
    for prop in required_properties:
        # print(auto_tags.get("father").handle(db, str(user_id)))
        properties[prop] = auto_tags.get(prop).handle(db, str(user_id))
        
    role = Authorize.get_raw_jwt()['role']
    document = await hr_document_service.generate_document_for_expiring_contract(db, contract_id, role, properties, years)
    return document

@router.get('/generate_document_for_expiring_rank/{rank_contract_id}/', summary="Generate draft for expiring ranks")
async def generate_document_for_expiring_rank(*,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends(),
                                      rank_contract_id: str = None,
                                      ):
    """
        Generate draft for expiring ranks

    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    properties = {}
    # {"rank": {"alias_name": "\u0417\u0432\u0430\u043d\u0438\u0435", "alias_nameKZ": "\u0414\u04d9\u0440\u0435\u0436\u0435", "data_taken": "auto", "type": "read", "data_type": null, "field_name": "rank", "to_tags": {"prevWordKZ": "{{real-rank-full}}", "alias_name": null, "alias_nameKZ": "rank", "directory": null, "isHidden": false, "cases": 0}}, "surname": {"alias_name": "\u0424\u0430\u043c\u0438\u043b\u0438\u044f \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430", "alias_nameKZ": "\u0422\u0435\u0433\u0456", "data_taken": "auto", "type": "read", "data_type": null, "field_name": "surname", "to_tags": {"prevWordKZ": "{{surname}}", "alias_name": null, "alias_nameKZ": "surname", "directory": null, "isHidden": false, "cases": 0}}, "name": {"alias_name": "\u0418\u043c\u044f \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430", "alias_nameKZ": "\u0410\u0442\u044b", "data_taken": "auto", "type": "read", "data_type": null, "field_name": "name", "to_tags": {"prevWordKZ": "{{name}}", "alias_name": null, "alias_nameKZ": "name", "directory": null, "isHidden": false, "cases": 0}}, "father": {"alias_name": "\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430", "alias_nameKZ": "\u04d8\u043a\u0435\u0441\u0456\u043d\u0456\u04a3 \u0430\u0442\u044b", "data_taken": "auto", "type": "read", "data_type": null, "field_name": "father_name", "to_tags": {"prevWordKZ": "{{father-name}}", "alias_name": null, "alias_nameKZ": "father", "directory": null, "isHidden": false, "cases": 0}}, "officer": {"alias_name": "\u041e\u0444\u0438\u0446\u0435\u0440\u0441\u043a\u0438\u0439 \u043d\u043e\u043c\u0435\u0440 \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430", "alias_nameKZ": "\u0421\u0443\u0431\u044a\u0435\u043a\u0442 \u049b\u044b\u0437\u043c\u0435\u0442\u043a\u0435\u0440\u0456\u043d\u0456\u04a3 \u043d\u04e9\u043c\u0456\u0440\u0456", "data_taken": "auto", "type": "read", "data_type": null, "field_name": "officer_number", "to_tags": {"prevWordKZ": "{{officer-number}}", "alias_name": null, "alias_nameKZ": "officer", "directory": null, "isHidden": false, "cases": 0}}, "new_rank": {"alias_name": "\u0417\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f", "alias_nameKZ": "\u0410\u0440\u0442\u0442\u044b\u0440\u0443 \u04af\u0448\u0456\u043d \u0414\u04d9\u0440\u0435\u0436\u0435", "data_taken": "dropdown", "type": "write", "data_type": null, "field_name": "rank", "to_tags": {"prevWordKZ": "{{new-rank-full}}", "alias_name": "\u0417\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f", "alias_nameKZ": "\u0410\u0440\u0442\u0442\u044b\u0440\u0443 \u04af\u0448\u0456\u043d \u0414\u04d9\u0440\u0435\u0436\u0435", "directory": "rank", "isHidden": false, "cases": null, "actions": [{"id": 0, "actions": {"args": [{"increase_rank": {"rank": {"tagname": "rank", "alias_name": "\u0417\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f", "alias_nameKZ": "\u0410\u0440\u0442\u0442\u044b\u0440\u0443 \u04af\u0448\u0456\u043d \u0414\u04d9\u0440\u0435\u0436\u0435"}}}]}, "properties": {"rank": {"alias_name": "\u0417\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f", "alias_nameKZ": "\u0410\u0440\u0442\u0442\u044b\u0440\u0443 \u04af\u0448\u0456\u043d \u0414\u04d9\u0440\u0435\u0436\u0435", "type": "write", "data_taken": "dropdown", "field_name": "rank"}}, "actionsValue": {"name": "\u041f\u0440\u0438\u0441\u0432\u043e\u0435\u043d\u0438\u0435 \u0437\u0432\u0430\u043d\u0438\u044f", "nameKZ": "\u0414\u04d9\u0440\u0435\u0436\u0435 \u0442\u0430\u0493\u0430\u0439\u044b\u043d\u0434\u0430\u0443"}}]}}, "extraordinary": {"alias_name": null, "alias_nameKZ": "extraordinary", "data_taken": "manual", "type": "read", "data_type": "string", "field_name": "manual", "to_tags": {"prevWordKZ": "{{first-officer-or-ordinary-or-extraordinary}}", "alias_name": null, "alias_nameKZ": "extraordinary", "directory": null, "isHidden": false, "cases": null}}, "military": {"alias_name": null, "alias_nameKZ": "military", "data_taken": "manual", "type": "read", "data_type": "string", "field_name": "manual", "to_tags": {"prevWordKZ": "{{special-or-military}}", "alias_name": null, "alias_nameKZ": "military", "directory": null, "isHidden": false, "cases": null}}}
    # required_properties = ["father_name", "name", "officer_number", "position", "rank", "surname"]
    required_properties = ["father_name", "name", "officer_number", "surname", "new_rank"]
    for prop in required_properties:
        properties[prop] = auto_tags.get(prop).handle(db, str(user_id))
        
    role = Authorize.get_raw_jwt()['role']
    document = await hr_document_service.generate_document_for_expiring_ranks(db, rank_contract_id, role, properties)
    return document