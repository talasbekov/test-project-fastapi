from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import SurveyRepeatTypeEnum

router = APIRouter(
    prefix="/survey_repeat_type",
    tags=["SurveyRepeatType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all SurveyRepeatType")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SurveyRepeatTypeEnum (Виды повторения опроса)

    """
    Authorize.jwt_required()
    return [ag.value for ag in SurveyRepeatTypeEnum]