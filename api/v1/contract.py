import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (ContractCreate,
                     ContractUpdate,
                     ContractRead,
                     ContractTypeRead,
                     ContractTypeReadPagination)
from services import contract_service

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=ContractRead,
            summary="Get all Ranks")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Ranks

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return contract_service.get_multi(db, skip, limit)

@router.get("/types", status_code=status.HTTP_200_OK,
            dependencies=[Depends(HTTPBearer())],
            response_model=ContractTypeReadPagination,
            summary="Get all Contract Types")
async def get_all_contract_types(*,
                                 db: Session = Depends(get_db),
                                 skip: int = 0,
                                 limit: int = 100,
                                 filter: str = '',
                                 Authorize: AuthJWT = Depends()
                                ):
    """
       Get all Contract Types

       - **skip**: int - The number of contract types
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of contract types
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return contract_service.get_all_contract_types(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ContractRead,
             summary="Create Rank")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ContractCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Rank

        - **name**: required
    """
    Authorize.jwt_required()
    return contract_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ContractRead,
            summary="Get Rank by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Rank by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return contract_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ContractRead,
            summary="Update Rank")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ContractUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Rank

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return contract_service.update(
        db,
        db_obj=contract_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Rank")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Rank

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    contract_service.remove(db, str(id))

@router.post("/types", status_code=status.HTTP_200_OK,
             dependencies=[Depends(HTTPBearer())],
             summary="Create contract type")
async def create_contract_type(*,
                               db: Session = Depends(get_db),
                               isFinite: bool,
                               years: int,
                               name: str,
                               nameKZ: str,
                               Authorize: AuthJWT = Depends()
                               ):
    return contract_service.create_contract_type(db, isFinite, years, name, nameKZ)