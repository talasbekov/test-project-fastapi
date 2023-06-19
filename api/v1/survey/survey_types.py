from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import SurveyTypeEnum

router = APIRouter(prefix="/survey_type", tags=["SurveyTypeEnum"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all SurveyTypeEnum")
async def get_all(*,
    Authorize: AuthJWT = Depends()
):
    """
        Get all SurveyTypeEnumEnum

    """
    Authorize.jwt_required()
    return [ag.value for ag in SurveyTypeEnum]
