from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
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
    return auto_tags.get(auto_tag).handle(db, user_id)
