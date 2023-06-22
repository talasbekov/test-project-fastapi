import uuid

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
import pymorphy2
from core import get_db

from models import LanguageEnum
from services import render_service

morph = pymorphy2.MorphAnalyzer()

class ConvertCandidateTemplate(BaseModel):
    hr_document_template_id: uuid.UUID
    candidate_id: uuid.UUID


router = APIRouter(
    prefix="/render",
    tags=["Render Jinja"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.post("/render", 
             dependencies=[Depends(HTTPBearer())],
             summary="Генерация документа 'Заключение спец. проверки'")
async def generate(*,
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
    return render_service.generate(
        db, 
        candidate_id=body.candidate_id, 
        template_id=body.hr_document_template_id)


@router.post("/render/finish-candidate", 
             dependencies=[Depends(HTTPBearer())],
             summary="Генерация документа 'Заключение на зачисление'")
async def render_finish_candidate(*,
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
    return await (render_service
                  .generate_finish_candidate(db=db, 
                                             candidate_id=body.candidate_id, 
                                             template_id=body.hr_document_template_id))


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


@router.post('/convert/pdf')
async def convert_html_to_pdf(*,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends(),
                              body: HTML
                              ):
    Authorize.jwt_required()
    return render_service.convert_html_to_pdf(body.html)


@router.get('/inflect')
async def inflect_word(
                    word: str, 
                    septik_int: int, 
                    lang: LanguageEnum = LanguageEnum.ru):
    if lang == LanguageEnum.ru:
        return padezh(word, septik_int)
    elif lang == LanguageEnum.kz:
        return septik(word, septik_int)
    else:
        return None


def septik(text, septik):
    text = text.lower()
    vowels = 'аәеэёоөұүыіуияю'
    hard = 'аоыұуияюё'
    consonants = 'жзкқлмнңпрстфхцчшщ'
    deaf = 'кқпстфхцчшщбвгдғ'
    last_char = text[-1]
    last_vowel = next(
        (char for char in reversed(text) if char in vowels),
        None)
    last_consonant = next(
        (char for char in reversed(text) if char in consonants), None)
    last_is_vowel = last_char in vowels
    if septik == 0:
        return text
    if septik == 1:
        if last_is_vowel:
            end = 'дАЕн'
        elif last_consonant in deaf:
            end = 'тАЕн'
        elif last_consonant in 'лрйжз':
            end = 'дАЕн'
        elif last_consonant in 'мнң':
            end = 'нАЕн'
    elif septik == 2:
        end = 'тАЕ' if last_consonant in deaf else 'дАЕ'
    elif septik == 3:
        end = 'гАЕ' if last_consonant in deaf else 'кАЕ'
    elif septik == 4:
        if last_char in 'июлруйжз':
            end = 'дЫІң'
        elif last_consonant in deaf:
            end = 'тЫІң'
        else:
            end = 'нЫІң'
    elif septik == 5:
        if last_char in 'июжзрлймнң':
            end = 'дЫІ'
        elif last_consonant in deaf:
            end = 'тЫІ'
        else:
            end = 'нЫІ'
    elif septik == 6:
        if last_char in 'жз':
            end = 'бен'
        elif last_consonant in deaf:
            end = 'пен'
        else:
            end = 'мен'
    else:
        end = ''
    if 'кАЕ' in end:
        end = end.replace(
            'кАЕ',
            'қа') if last_vowel in hard else end.replace(
            'АЕ',
            'е')
    elif 'гАЕ' in end:
        end = end.replace(
            'гАЕ',
            'ға') if last_vowel in hard else end.replace(
            'АЕ',
            'е')
    elif 'АЕ' in end:
        end = end.replace(
            'АЕ',
            'а') if last_vowel in hard else end.replace(
            'АЕ',
            'е')
    elif 'ЫІ' in end:
        end = end.replace(
            'ЫІ',
            'ы') if last_vowel in hard else end.replace(
            'ЫІ',
            'і')
    return text + end

def padezh(word, septik_int):
    parsed_word = morph.parse(word)
    if septik_int == 1:
        return parsed_word.inflect({'gent'}).word
    if septik_int == 2:
        return parsed_word.inflect({'datv'}).word
    if septik_int == 3:
        return parsed_word.inflect({'accs'}).word
    if septik_int == 4:
        return parsed_word.inflect({'loc2'}).word
    if septik_int == 5:
        return parsed_word.inflect({'gen2'}).word
    if septik_int == 6:
        return parsed_word.inflect({'ablt'}).word
    return word
