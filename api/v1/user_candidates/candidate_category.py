from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from services import candidate_category_service

router = APIRouter(
    prefix="/candidate_categories",
    tags=["CandidateCategory"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all CandidateCategory")
async def get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all CandidateCategory

        - **skip**: int - The number of CandidateCategory to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateCategory to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_category_service.get_multi(db, skip, limit)
