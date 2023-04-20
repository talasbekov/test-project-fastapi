import uuid

from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from core import get_db

from services import render_service


class ConvertCandidateTemplate(BaseModel):
    hr_document_template_id: uuid.UUID
    candidate_id: uuid.UUID


router = APIRouter(prefix="/render", tags=["Render Jinja"], dependencies=[Depends(HTTPBearer())])


@router.post("/render", dependencies=[Depends(HTTPBearer())])
async def convert(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: ConvertCandidateTemplate
):
    """
        Генерация документа "Заключение спец. проверки"

        - **hr_document_template_id**: UUID - required
        - **candidate_id**: UUID - required
    """
    Authorize.jwt_required()
    return render_service.generate(db, candidate_id=body.candidate_id, template_id=body.hr_document_template_id)

@router.post("/render/finish-candidate", dependencies=[Depends(HTTPBearer())])
async def rdner_finish_candidate(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: ConvertCandidateTemplate
):
    """
        Генерация документа "Заключение на зачисление"

        - **hr_document_template_id**: UUID - required
        - **candidate_id**: UUID - required
    """
    Authorize.jwt_required()
    return render_service.generate_finish_candidate(db, candidate_id=body.candidate_id, template_id=body.hr_document_template_id)


class HTML(BaseModel):
    html: str

@router.post('/convert', dependencies=[Depends(HTTPBearer())])
async def convert(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: HTML
):
    Authorize.jwt_required()
    return render_service.convert_html_to_docx(body.html)


@router.post('/convert_docx_to_html', dependencies=[Depends(HTTPBearer())])
async def convert_docx_to_html(*,
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    return render_service.convert_docx_to_xml_to_html()
