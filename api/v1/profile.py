import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import Profile
from schemas import ProfileRead, ProfileUpdate
from services import profile_service

router = APIRouter(prefix="/profile",
                   tags=["Profiles"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ProfileRead],
            summary="Get all Profiles")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Profiles

    """
    Authorize.jwt_required()
    return profile_service.get_multi(db, skip, limit)


# @router.get("/personal_document",
#             dependencies=[Depends(HTTPBearer())],
#             summary="Get Profile Document by user_id")
# async def get_document_by_user(*,
#                                db: Session = Depends(get_db),
#                                user_id: str,
#                                Authorize: AuthJWT = Depends()
#                                ):
#     """
#         Get profile document by user_id

#         - **id**: UUID - required.
#     """
#     Authorize.jwt_required()
#     generated_file_data = profile_service.generate_profile_doc(db, str(user_id))

# return FileResponse(path=generated_file_data["file_location"],
# media_type='application/octet-stream',
# filename=generated_file_data["file_name"])


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ProfileRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new profile

        no parameters required.
    """
    Authorize.jwt_required()
    profile = db.query(Profile).filter(Profile.user_id ==
                                       Authorize.get_jwt_subject()).first()
    if profile is not None:
        return profile
    return profile_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ProfileRead,
            summary="Get Profile by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get profile by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return profile_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ProfileRead,
            summary="Update Profile")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ProfileUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Profile

    """
    Authorize.jwt_required()
    return profile_service.update(
        db,
        db_obj=profile_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Profile")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Profile

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    profile_service.remove(db, str(id))
