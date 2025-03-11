import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    EquipmentCreate,
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
    TypeClothingEquipmentUpdate
)
from schemas.equipment import (
    TypeArmyEquipmentModel,
    TypeOtherEquipmentRead,
    TypeOtherEquipmentModel,
    TypeClothingEquipmentRead,
    TypeClothingEquipmentModelSchema
)
from services.equipment import equipment_service

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
    dependencies=[Depends(HTTPBearer())]
)


@router.get("",
            dependencies=[Depends(HTTPBearer())],
            response_model=List[EquipmentRead],
            summary="Get all Equipments")
async def get_all(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return equipment_service.get_multi(db, skip, limit)


@router.post("",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=EquipmentCreate,
             summary="Create Equipment")
async def create(
    db: Session = Depends(get_db),
    body: EquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create(db, body)


@router.get("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Get Equipment by id")
async def get_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_by_id(db, str(id))


@router.put("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Update Equipment")
async def update(
    db: Session = Depends(get_db),
    id: str = None,
    body: EquipmentUpdate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update(db=db, id=id, body=body)


@router.delete("/{id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Equipment")
async def delete(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    equipment_service.remove(db, str(id))


# ------------------- Одежда (Clothing) ------------------- #

@router.get("/type/clothing/",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeClothingEquipmentReadPagination,
            summary="Get all Clothing Equipments")
async def get_all_clothing_types(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return equipment_service.get_all_clothing_equipments(db, skip, limit)


@router.get("/type/clothing/{id}",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeClothingEquipmentRead,
            summary="Get Clothing Equipment type by id")
async def get_clothing_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_clothing_equipment_type_by_id(db, id)


@router.put("/type/clothing/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Clothing Equipment type")
async def update_type_clothing(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeClothingEquipmentUpdate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_type_clothing(db, id, body)


@router.delete("/type/clothing/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Clothing Equipment type")
async def delete_type_clothing(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_type_clothing(db, id)


@router.post("/type/clothing/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeClothingEquipmentRead,
             summary="Create Clothing Equipments Type")
async def create_cloth_eq_type(
    db: Session = Depends(get_db),
    body: TypeClothingEquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_cloth_eq_type(db, body)


@router.get("/model/clothing/",
            dependencies=[Depends(HTTPBearer())],
            response_model=List[TypeClothingEquipmentModelSchema],
            summary="Get all Clothing Equipments Models")
async def get_all_clothing_models(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_all_clothing_equipment_models(db)


@router.post("/model/clothing/",
             dependencies=[Depends(HTTPBearer())],
             summary="Create Clothing Equipments Model")
async def create_cloth_eq_model(
    db: Session = Depends(get_db),
    body: TypeClothingEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_cloth_eq_model(db, body)


@router.get("/models/clothing/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Get Clothing Equipment Model by id")
async def get_cloth_model_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_clothing_equipment_model_by_id(db, id)


@router.put("/models/clothing/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Clothing Equipment Model")
async def update_cloth_model(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeClothingEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_cloth_model(db, id, body)


@router.delete("/models/clothing/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Clothing Equipment Model")
async def delete_cloth_model(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_cloth_model(db, id)


# ------------------- Армейское (Army) ------------------- #

@router.get("/type/army/",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeArmyEquipmentReadPagination,
            summary="Get all Army Equipments")
async def get_all_army(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10,
    filter: str = ''
):
    Authorize.jwt_required()
    return equipment_service.get_all_army_equipments(db, skip, limit, filter)


@router.get("/type/army/{id}",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeArmyEquipmentRead,
            summary="Get Army Equipment type by id")
async def get_army_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_army_equipment_type_by_id(db, id)


@router.put("/type/army/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Army Equipment type")
async def update_type_army(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeArmyEquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_type_army(db, id, body)


@router.delete("/type/army/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Army Equipment type")
async def delete_type_army(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_type_army(db, id)


@router.post("/type/army/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeArmyEquipmentRead,
             summary="Create Army Equipments Type")
async def create_army_eq_type(
    db: Session = Depends(get_db),
    body: TypeArmyEquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_army_eq_type(db, body)


@router.post("/model/army/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeArmyEquipmentModel,
             summary="Create Army Equipments Model")
async def create_army_eq_model(
    db: Session = Depends(get_db),
    body: TypeArmyEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_army_eq_model(db, body)


@router.get("/models/army",
            dependencies=[Depends(HTTPBearer())],
            summary="Get all Models of Army Equipments")
async def get_all_army_models(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_all_army_equipment_models(db)


@router.get("/models/army/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Get Army Equipment Model by id")
async def get_army_model_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_army_equipment_model_by_id(db, id)


@router.put("/models/army/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Army Equipment Model")
async def update_army_model(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeArmyEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_army_model(db, id, body)


@router.delete("/models/army/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Army Equipment Model")
async def delete_army_model(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_army_model(db, id)


# ------------------- Прочее оборудование (Other) ------------------- #

@router.get("/type/other/",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeOtherEquipmentReadPagination,
            summary="Get all Other Equipments")
async def get_all_other(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10,
    filter: str = ''
):
    Authorize.jwt_required()
    return equipment_service.get_all_other_equipments(db, skip, limit, filter)


@router.get("/type/other/{id}",
            dependencies=[Depends(HTTPBearer())],
            response_model=TypeOtherEquipmentRead,
            summary="Get Other Equipment type by id")
async def get_other_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_other_equipment_type_by_id(db, id)


@router.post("/type/other/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeOtherEquipmentRead,
             summary="Create Other Equipments Type")
async def create_other_eq_type(
    db: Session = Depends(get_db),
    body: TypeOtherEquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_other_eq_type(db, body)


@router.put("/type/other/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Other Equipment Type")
async def update_other_type(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeOtherEquipmentCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_other_type(db, id, body)


@router.delete("/type/other/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Other Equipment Type")
async def delete_other_type(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_other_type(db, id)


@router.post("/model/other/",
             dependencies=[Depends(HTTPBearer())],
             response_model=TypeOtherEquipmentModel,
             summary="Create Other Equipments Model")
async def create_other_eq_model(
    db: Session = Depends(get_db),
    body: TypeOtherEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create_other_eq_model(db, body)


@router.get("/models/other",
            dependencies=[Depends(HTTPBearer())],
            summary="Get all Models of Other Equipments")
async def get_all_other_models(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_all_other_equipment_models(db)


@router.get("/models/other/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Get Other Equipment Model by id")
async def get_other_model_by_id(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.get_other_equipment_model_by_id(db, id)


@router.put("/models/other/{id}",
            dependencies=[Depends(HTTPBearer())],
            summary="Update Other Equipment Model")
async def update_other_model(
    db: Session = Depends(get_db),
    id: str = None,
    body: TypeOtherEquipmentModelCreate = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update_other_model(db, id, body)


@router.delete("/models/other/{id}",
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Other Equipment Model")
async def delete_other_model(
    db: Session = Depends(get_db),
    id: str = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.delete_other_model(db, id)


# ------------------- Получение всех моделей ------------------- #

@router.get("/models/all",
            dependencies=[Depends(HTTPBearer())],
            summary="Get all Models of Equipments")
async def get_all_models(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    res = []
    res.extend(equipment_service.get_all_clothing_equipment_models(db))
    res.extend(equipment_service.get_all_army_equipment_models(db))
    res.extend(equipment_service.get_all_other_equipment_models(db))
    return res


@router.get("/type/all",
            dependencies=[Depends(HTTPBearer())],
            response_model=List[str],
            summary="Get all Types of Equipments")
async def get_all_types(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return ["other_equipment", "clothing_equipment", "army_equipment"]
