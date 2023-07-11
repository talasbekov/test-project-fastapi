from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import SurveyStaffPositionEnum

router = APIRouter(
    prefix="/survey_staff_position",
    tags=["SurveyStaffPosition"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all SurveyStaffPosition")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SurveyStaffPosition (Служебное положение опроса)

    """
    Authorize.jwt_required()
    return [ag.value for ag in SurveyStaffPositionEnum]