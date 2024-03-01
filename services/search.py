from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from .user import user_service
from services import general_user_information_service, service_id_service, staff_division_service, staff_unit_service
from sqlalchemy import inspect, or_, String
from schemas.search import Search, SearchTypeListRead, SearchTypeListCreate


models = {
    "general_user_information": general_user_information_service.model,
    "service_id": service_id_service.model,
    "general" : user_service.model,
    "staff_division": staff_division_service.model,
    "staff_unit": staff_unit_service.model
}

class SearchService:

    async def general(self, db: Session, params: SearchTypeListCreate, skip: int = 0, limit: int = 100):
        for param in params.search_types:
            type_name = param.search_type
            name = param.name
            if type_name not in models:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type is not found!")
            model = models[type_name]
            qr = self.filter_model(model, skip, limit, db, name)
            if type_name == "general":
                qr = await self._find_users_by_ids(db, [qr.id for qr in qr])
            else:
                qr = SearchTypeListRead(**{type_name: [Search(user_id=qr.id, name=qr.name if hasattr(model, 'name') else None) for qr in qr]})
            return qr
    def filter_model(self, model, skip: int = 0, limit: int = 100, db: Session = None, name: str = None):
        filters = [
            self.set_filter(model, column, name)
            for column in inspect(model).columns
        ]
        qr = db.query(model).filter(or_(*filters)).offset(skip).limit(limit).all()
        return qr


    def set_filter(self,model, column, name: str = None):
        if isinstance(name, str):
            return getattr(model, column.key).ilike(f"%{name}%")
        if isinstance(name, list):
            return getattr(model, column.key).in_(name)
        return getattr(model, column.key) == name

    async def _find_users_by_ids(self, db: Session, user_ids: List[int]):
        model = user_service.model
        qr = db.query(model).filter(model.id.in_(user_ids)).all()
        return SearchTypeListRead(users=[Search(user_id=qr.id, name=qr.first_name + " " + qr.last_name if qr.last_name is not None else "") for qr in qr])



search_service = SearchService()
