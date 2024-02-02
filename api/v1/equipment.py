import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (EquipmentCreate,
                     EquipmentUpdate,
                     EquipmentRead,
                     TypeClothingEquipmentReadPagination,
                     TypeArmyEquipmentReadPagination,
                     TypeOtherEquipmentReadPagination,
                     TypeArmyEquipmentRead,
                     TypeArmyEquipmentCreate,
                     TypeArmyEquipmentModelCreate,
                     TypeClothingEquipmentCreate,
                     TypeClothingEquipmentModelCreate,
                     TypeOtherEquipmentCreate,
                     TypeOtherEquipmentModelCreate,
                     )
from schemas.equipment import (TypeArmyEquipmentModel,
                               TypeOtherEquipmentRead,
                               TypeOtherEquipmentModel,
                               TypeClothingEquipmentRead,
                               TypeClothingEquipmentModel,)
from services import equipment_service

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[EquipmentRead],
            summary="Get all Equipments")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
        Get all Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=EquipmentCreate,
             summary="Create Equipment")
async def create(*,
                 db: Session = Depends(get_db),
                 body: EquipmentCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Equipment

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return equipment_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Get Equipment by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
       Get Equipment by id

       - **id**: UUID - required
    """
    Authorize.jwt_required()
    return equipment_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Update Equipment")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: EquipmentUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Equipment

        - **id**: UUID - the id of equipment to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return equipment_service.update(
        db=db,
        id=id,
        body=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Equipment")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Equipment

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    equipment_service.remove(db, str(id))


@router.get("/type/clothing/", dependencies=[Depends(HTTPBearer())],
            response_model=TypeClothingEquipmentReadPagination,
            summary="Get all Clothing Equipments")
async def get_all_clothing(*,
                           db: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends(),
                           skip: int = 0,
                           limit: int = 10
                           ):
    """
        Get all Clothing Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_all_clothing_equipments(db, skip, limit)


@router.get("/model/clothing/", dependencies=[Depends(HTTPBearer())],
            response_model=List[TypeClothingEquipmentModel],
            summary="Get all Clothing Equipments")
async def get_all_clothing(*,
                           db: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends()
                           ):
    """
        Get all Clothing Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_all_clothing_equipment_models(db)


@router.get("/type/army/", dependencies=[Depends(HTTPBearer())],
            response_model=TypeArmyEquipmentReadPagination,
            summary="Get all Army Equipments")
async def get_all_army(*,
                       db: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends(),
                       skip: int = 0,
                       limit: int = 10,
                       filter: str = ''
                       ):
    """
        Get all Army Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_all_army_equipments(db, skip, limit, filter)


@router.get("/type/other/", dependencies=[Depends(HTTPBearer())],
            response_model=TypeOtherEquipmentReadPagination,
            summary="Get all Other Equipments")
async def get_all_other(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        skip: int = 0,
                        limit: int = 10,
                        filter: str = ''
                        ):
    """
        Get all Other Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_all_other_equipments(db, skip, limit, filter)


@router.get("/type/all", dependencies=[Depends(HTTPBearer())],
            response_model=List[str],
            summary="Get all Types of Equipments")
async def get_all_types(*,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(),
                        skip: int = 0,
                        limit: int = 10
                        ):
    """
        Get all Types of Equipments

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return ["other_equipment", "clothing_equipment", "army_equipment"]


@router.get("available/{user_id}/", dependencies=[Depends(HTTPBearer())],
            summary="Get all available Equipments for user")
async def get_all_available(*,
                            db: Session = Depends(get_db),
                            user_id: str,
                            Authorize: AuthJWT = Depends(),
                            skip: int = 0,
                            limit: int = 10
                            ):
    """
        Get all available Equipments for user

        - **skip**: int - The number of equipments to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_all_available_equipments(
        db, user_id, skip, limit)


@router.post("/type/other/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeOtherEquipmentRead,
             summary="Create Other Equipments Type")
async def create_other_eq_type(*,
                               db: Session = Depends(get_db),
                               Authorize: AuthJWT = Depends(),
                               body: TypeOtherEquipmentCreate
                               ):
    Authorize.jwt_required()
    return equipment_service.create_other_eq_type(db, body)


@router.post("/model/other/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeOtherEquipmentModel,
             summary="Create Other Equipments Model")
async def create_other_eq_model(*,
                                db: Session = Depends(get_db),
                                Authorize: AuthJWT = Depends(),
                                body: TypeOtherEquipmentModelCreate
                                ):
    Authorize.jwt_required()
    return equipment_service.create_other_eq_model(db, body)


@router.post("/type/army/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeArmyEquipmentRead,
             summary="Create Army Equipments Type")
async def create_army_eq_type(*,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends(),
                              body: TypeArmyEquipmentCreate
                              ):
    Authorize.jwt_required()
    return equipment_service.create_army_eq_type(db, body)


@router.post("/model/army/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeArmyEquipmentModel,
             summary="Create Army Equipments Model")
async def create_army_eq_model(*,
                               db: Session = Depends(get_db),
                               Authorize: AuthJWT = Depends(),
                               body: TypeArmyEquipmentModelCreate
                               ):
    Authorize.jwt_required()
    return equipment_service.create_army_eq_model(db, body)


@router.post("/type/clothing/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeClothingEquipmentRead,
             summary="Create Army Equipments Type")
async def create_cloth_eq_type(*,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends(),
                              body: TypeClothingEquipmentCreate
                              ):
    Authorize.jwt_required()
    return equipment_service.create_cloth_eq_type(db, body)


@router.post("/model/clothing/",
             dependencies=[Depends(HTTPBearer())],
             summary="Create Army Equipments Model")
async def create_cloth_eq_model(*,
                               db: Session = Depends(get_db),
                               Authorize: AuthJWT = Depends(),
                               body: TypeClothingEquipmentModelCreate
                               ):
    Authorize.jwt_required()
    return equipment_service.create_cloth_eq_model(db, body)
