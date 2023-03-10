from sqlalchemy.orm import Session
from services import ServiceBase

from exceptions import client
from models import StaffList
from schemas import StaffListCreate,StaffListRead,StaffListUpdate

class StaffListService(ServiceBase[StaffList,StaffListCreate,StaffListUpdate]):

    def get_by_id(self,db: Session,id: str):
        staff_list = super().get(db,id)
        if staff_list is None:
            raise client.NotFoundException(detail="Staff list is not found!")
        return staff_list
    
    def create_by_user_id(self,db: Session,*,user_id: str, obj_in: StaffListCreate):

        db_obj = obj_in.dict()

        db_obj['user_id'] = user_id

        staff_list = super().create(db,db_obj)
        return staff_list

staff_list_service = StaffListService(StaffList)
