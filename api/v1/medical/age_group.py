from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import AgeGroup

router = APIRouter(
    prefix="/age_group",
    tags=["AgeGroup"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all AgeGroup")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all AgeGroupEnum

    """
    Authorize.jwt_required()
    return [ag.value for ag in AgeGroup]
