import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (StaffDivisionCreate, StaffDivisionReadMinimized, StaffDivisionRead,
                     StaffDivisionStepRead, StaffDivisionUpdate,
                     StaffDivisionUpdateParentGroup, StaffDivisionTypeRead, StaffDivisionReadSchedule,
                     StaffDivisionMatreshkaStepRead, StaffDivisionNamedModel)
from services import staff_division_service, staff_division_type_service

router = APIRouter(
    prefix="/staff_division",
    tags=["StaffDivision"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Staff Divisions

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return staff_division_service.get_all_except_special(db, skip, limit)

@router.get("/schedule/", dependencies=[Depends(HTTPBearer())],
            # response_model=List[StaffDivisionReadSchedule],
            summary="Get all Staff Divisions")
async def get_all_schedule(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Staff Divisions

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return staff_division_service.get_all_except_special_schedule(db, skip, limit)


@router.get("/departments/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_departments(*,
                          db: Session = Depends(get_db),
                          skip: int = 0,
                          limit: int = 100,
                          Authorize: AuthJWT = Depends()
                          ):
    """
       Get all Staff Divisions

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_division_service.get_all_departments(db, skip, limit)


@router.get("/division_parents/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
            summary="Get Staff Division and all his parents")
async def get_division_parents_by_id(*,
                                     db: Session = Depends(get_db),
                                     id: str,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
       Get all Staff Divisions

       - **id**: uuid - The id of staff division. This parameter is required.
   """
    Authorize.jwt_required()
    return staff_division_service.get_division_parents_by_id(db, str(id))

@router.get("/division_parents_minimized/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionReadMinimized,
            summary="Get Staff Division and all his parents with fewer parameters")
async def get_division_parents_by_id_minimized(*,
                                     db: Session = Depends(get_db),
                                     id: str,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
       Get all Staff Divisions

       - **id**: uuid - The id of staff division. This parameter is required.
   """
    Authorize.jwt_required()
    return staff_division_service.get_division_parents_by_id_minimized(db, str(id))


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffDivisionRead,
             summary="Create Staff Division")
async def create(*,
                 db: Session = Depends(get_db),
                 body: StaffDivisionCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Staff Division

        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_division_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
            summary="Get Staff Division by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return staff_division_service.get_by_id(db, str(id))

@router.get("/schedule/{id}/", dependencies=[Depends(HTTPBearer())],
            # response_model=StaffDivisionReadSchedule,
            summary="Get Staff Division by id")
async def get_by_id_schedule(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return staff_division_service.get_by_id_schedule(db, str(id))


@router.get("/get-department-of/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionNamedModel,
            summary="Get Staff Division one level by id")
async def get_all_one_level_for_id(*,
                                   db: Session = Depends(get_db),
                                   id: str,
                                   Authorize: AuthJWT = Depends()
                                   ):
    """
       Get Department of staff division

    - **id**: uuid - The id of staff division. This parameter is required.
    """
    Authorize.jwt_required()
    return staff_division_service.get_department_name_by_id(db, str(id))


@router.get("/one-level/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionStepRead,
            summary="Get Staff Division one level by id")
async def get_all_one_level_for_id(*,
                                   db: Session = Depends(get_db),
                                   id: str,
                                   Authorize: AuthJWT = Depends()
                                   ):
    """
       Get all Staff Divisions

    - **id**: uuid - The id of staff division. This parameter is required.
    """
    Authorize.jwt_required()
    return staff_division_service.get_by_id(db, str(id))


@router.get("/one-level-matreshka", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionMatreshkaStepRead,
            summary="Get Staff Division one level by id")
async def get_all_one_level_for_id(*,
                                   db: Session = Depends(get_db),
                                   id: Optional[str] = None,
                                   Authorize: AuthJWT = Depends()
                                   ):
    """
       Get all Staff Divisions

    - **id**: uuid - The id of staff division. This parameter is required.
    """
    Authorize.jwt_required()
    return staff_division_service.get_one_level_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
            summary="Update Staff Division")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: StaffDivisionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Staff Division

        - **id**: UUID - id of the Staff Division.
        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_division_service.update(
        db, db_obj=staff_division_service.get_by_id(db, str(id)), obj_in=body)


@router.post("/{id}/", status_code=status.HTTP_202_ACCEPTED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffDivisionRead,
             summary="Update parent of Staff Division")
async def update_parent(*,
                        db: Session = Depends(get_db),
                        id: str,
                        body: StaffDivisionUpdateParentGroup,
                        Authorize: AuthJWT = Depends()
                        ):
    """
        Update parent of Staff Division

        - **id**: UUID - staff division id. It is required
        - **parent_group_id**: the id of the parent group. It is required
    """
    Authorize.jwt_required()
    return staff_division_service.change_parent_group(db, id, body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff Division")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authrorize: AuthJWT = Depends()
                 ):
    """
        Delete Staff Division

        - **id**: UUID - required
    """
    Authrorize.jwt_required()
    staff_division_service.delete(db, str(id))


@router.get('/name/{id}', dependencies=[Depends(HTTPBearer())],
            summary="Get Staff Division by id")
async def get_full_name_by_id(*,
                              db: Session = Depends(get_db),
                              id: str,
                              Authorize: AuthJWT = Depends()
                              ):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    full_name, full_nameKZ = staff_division_service.get_full_name(db, str(id))
    return {"name": full_name, "nameKZ": full_nameKZ}


@router.get("/types", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionTypeRead],
            summary="Get Staff Division types")
async def get_division_types(*,
                             db: Session = Depends(get_db),
                             skip: int = 0,
                             limit: int = 100,
                             Authorize: AuthJWT = Depends()
                             ):
    """
       Get all Staff Division Types
    """
    Authorize.jwt_required()
    return staff_division_type_service.get_multi(db, skip=skip, limit=limit)


@router.get('/ids/{id}/', dependencies=[Depends(HTTPBearer())],
            response_model=List[str],
            summary="Get ids of all parents of Staff Division")
async def get_parent_ids(*,
                         db: Session = Depends(get_db),
                         id: str,
                         Authorize: AuthJWT = Depends()
                         ):
    Authorize.jwt_required()
    return staff_division_service.get_parent_ids(db, str(id))

@router.get("/recursive", dependencies=[Depends(HTTPBearer())],
            # response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()
                  ):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return staff_division_service.build_staff_division_tree(db)

@router.get("/recursive/department", dependencies=[Depends(HTTPBearer())],
            # response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_all_by_department(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()
                  ):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return staff_division_service.build_staff_division_tree_until_department(db, user_id)

@router.get("/schedule_short", dependencies=[Depends(HTTPBearer())],
            # response_model=List[StaffDivisionReadSchedule],
            summary="Get all Staff Divisions")
async def get_all_schedule(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Staff Divisions

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return staff_division_service.get_all_except_special_schedule_short(db, skip, limit)

@router.get("/schedule_short/{id}/", dependencies=[Depends(HTTPBearer())],
            # response_model=StaffDivisionReadSchedule,
            summary="Get Staff Division by id short")
async def get_by_id_schedule(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return staff_division_service.get_by_id_schedule_short(db, str(id))

@router.get("/get_leader_id/{id}", dependencies=[Depends(HTTPBearer())],
            summary="Get Staff Division leader id")
async def get_leader_id(*,
                        db: Session = Depends(get_db),
                        id: str,
                        Authorize: AuthJWT = Depends()
                        ):
    """

    - **id**: UUID - required   
    """
    Authorize.jwt_required()
    return staff_division_service.get_leader_id(db, str(id))
