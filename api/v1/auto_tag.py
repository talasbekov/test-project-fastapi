from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from core import get_db
from services.autotags import auto_tags

router = APIRouter(
    prefix="/auto-tags",
    tags=["AutoTag"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("/{user_id}/")
async def get_by_user_id(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    auto_tag: str,
    Authorize: AuthJWT = Depends()
):
    """Get User data through AutoTag

    Args:
        user_id (str): id of user from whom data is to be fetched
        auto_tag (str): auto_tag to be used to fetch data
        db (Session, optional): Instance of Session for database connection.
        Defaults to Depends(get_db).
        Authorize (AuthJWT, optional): JWTToken holder class. Defaults to Depends().

    Returns:
        Any: Result from AutoTag
    """
    # auto_tag_handler = auto_tags.get(auto_tag)
    # if not auto_tag_handler:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Invalid auto_tag: {auto_tag}. Please provide a valid auto_tag."
    #     )
        
    # return auto_tag_handler.handle(db, str(user_id))
    return {
        "name": "СГО РК  Воинская часть 0112  5 управление  1 отдел  2 группа  () (Специалист 2 категории - пулеметчик)",
        "nameKZ": "СГО РК  Воинская часть 0112  5 управление  1 отдел  2 группа  () (Специалист 2 категории - пулеметчик)"
    }