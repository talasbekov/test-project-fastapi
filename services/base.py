from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core import Base
from exceptions import NotFoundException
from datetime import datetime
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ServiceBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """_summary_

        Base Service class with default methods to Create, Read, Update, Delete (CRUD).
        """

        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_id(self, db: Session, id: Any) -> ModelType:
        res = self.get(db, id)
        if res is None:
            raise NotFoundException(
                detail=f"{self.model.__name__} with id {id} not found!")
        return res

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session,
               obj_in: Union[CreateSchemaType, Dict[str, Any]],
               model: ModelType = None) -> ModelType:
        if model is None:
            model = self.model
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        setattr(db_obj, 'updated_at', datetime.now())
        db.add(db_obj)
        db.flush()
        return db_obj

    def remove(self, db: Session, id: str) -> ModelType:
        try:
            obj = db.query(self.model).get(id)
            if obj is None:
                raise NotFoundException(
                    detail=f"{self.model.__name__} with id {id} not found!")
            db.delete(obj)
            db.flush()
            return obj
        except Exception as e:
            db.rollback()
            raise e
