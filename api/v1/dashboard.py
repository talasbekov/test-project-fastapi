from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from services import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("/", dependencies=[Depends(HTTPBearer())],
            summary="Get all data for Dashboard")
async def get_all_state(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        ):
    """
       Get all Specialty Enum
   """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return dashboard_service.get_all_state(db, role)

    # ALL_STATE_VIEWERS = [
    #     PositionNameEnum.SUPERVISOR.value,
    #     PositionNameEnum.HEAD_OF_DEPARTMENT.value,
    #     PositionNameEnum.MANAGEMENT_HEAD.value,
    # ]
    #
    # def _check_by_role(self, db: Session, role_id: str) -> bool:
    #     """
    #         Checks if a user with the given role
    #         ID has permission to view number of all state of SGO RK.
    #     """
    #     staff_unit = staff_unit_service.get_by_id(db, role_id)
    #
    #     available_all_roles = [position_service.get_id_by_name(
    #         db, name) for name in self.ALL_STATE_VIEWERS]
    #
    #     return any(staff_unit.position_id == i for i in available_all_roles)
