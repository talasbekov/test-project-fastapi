import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect

from schemas import JoinRecordsBody


class DictionaryService:

    async def join_records(self,
                           db: Session,
                           entity: str,
                           body: JoinRecordsBody):
        """
        Updates all connected foreign key to correct_id

        Args:
            db (Session): db connection
            entity (str): entity which records will be joined
            body (JoinRecordsBody): request body with ids
        """
        # TODO: write consts for all cases
        TABLES = {
            'institutions': 'hr_erp_educations',
            'positions': 'hr_erp_positions'
        }

        COLUMNS = {
            'institutions': 'institution_id',
            'positions': 'hr_erp_positions'
        }

        query = text(f"UPDATE {TABLES[entity]} "
                     f"SET {COLUMNS[entity]} = '{body.correct_id}' "
                     f"WHERE {COLUMNS[entity]} = :id_to_change")
        for id_to_change in body.ids_to_change:
            db.execute(query, {'id_to_change': id_to_change})

    async def soft_update(self,
                          db: Session,
                          entity: str,
                          id: str):
        """
        Update record by creating changed duplicate and not changing existing 
        records. Record will be deactivated so it wouldn't be used in future.

        Args:
            db (Session): db connection
            entity (str): entity which records will be soft updated
            id (str): id to update
        """
        # TODO: write consts for all cases
        MODULES = {
            'institution': ('education', 'Institution')
        }

        package, class_name = MODULES[entity]
        module = __import__('models.' + package,
                            fromlist=[class_name])
        class_obj = getattr(module, class_name)

        current_obj = db.query(class_obj).filter(
            class_obj.id == id).first()

        new_obj = class_obj(**(await self.__get_column_values(current_obj)))
        new_obj.id = str(uuid.uuid4())
        new_obj.created_at = None
        new_obj.updated_at = None

        current_obj.active = 0

        db.add(new_obj)
        db.add(current_obj)
        db.flush()

    async def __get_column_values(self,
                                  obj) -> dict:
        """
        Get all columns and their values of sqlalchemy object.

        Args:
            obj: sqlalchemy object

        Returns:
            dict: {column: value...} dict 
        """
        obj_inspector = inspect(obj)
        columns = obj_inspector.mapper.column_attrs.keys()
        values = {column: getattr(obj, column) for column in columns}
        return values


dictionary_service = DictionaryService()
