from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import SurveyJurisdictionTypeEnum

router = APIRouter(
    prefix="/survey_jurisdiction_type",
    tags=["SurveyJurisdictionType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all SurveyJurisdictionType")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SurveyJurisdictionTypeEnum (Опрос проводится в рамках)

    """
    Authorize.jwt_required()
    return [ag.value for ag in SurveyJurisdictionTypeEnum]
