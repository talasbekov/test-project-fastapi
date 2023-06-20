from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import QuestionTypeEnum

router = APIRouter(prefix="/question_type",
                   tags=["QuestionTypeEnum"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all QuestionTypeEnum")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all QuestionTypeEnumEnum

    """
    Authorize.jwt_required()
    return [ag.value for ag in QuestionTypeEnum]
