from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from models import CandidateStageQuestionTypeEnum

router = APIRouter(
    prefix="/candidate_stage_question_type",
    tags=["CandidateStageQuestionTypeEnum"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all CandidateStageQuestionTypeEnum")
async def get_all(*,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all CandidateStageQuestionTypeEnumEnum

    """
    Authorize.jwt_required()
    return [ag.value for ag in CandidateStageQuestionTypeEnum]
