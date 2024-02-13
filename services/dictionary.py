import uuid
from datetime import datetime

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
        TABLES = {
            'institutions': 'hr_erp_educations',
            'positions': 'hr_erp_staff_units',
            'ranks': 'hr_erp_users',
            'badges': 'hr_erp_badges',
            'penalties': 'hr_erp_penalties',
            'properties': 'hr_erp_properties',
            'sports': 'hr_erp_sport_degrees',
            'statuses': 'hr_erp_statuses',
            'specialties': 'hr_erp_educations',
            'academic_degrees': 'hr_erp_academic_degrees',
            'academic_titles': 'hr_erp_academic_titles',
            'country': 'hr_erp_abroad_travels',
            'courses': 'hr_erp_courses',
            'inst_degrees': 'hr_erp_educations',
            'institutions': 'hr_erp_educations',
            'sciences': 'hr_erp_academic_degrees',
            'languages': 'hr_erp_language_proficiencies'
        }

        COLUMNS = {
            'institutions': 'institution_id',
            'positions': 'position_id',
            'ranks': 'rank_id',
            'badges': 'type_id',
            'penalties': 'type_id',
            'properties': 'type_id',
            'sports': 'sport_type_id',
            'statuses': 'type_id',
            'specialties': 'specialty_id',
            'academic_degrees': 'degree_id',
            'academic_titles': 'degree_id',
            'country': 'destination_country_id',
            'courses': 'course_provider_id',
            'inst_degrees': 'degree_id',
            'institutions': 'institution_id',
            'sciences': 'science_id',
            'languages': 'language_id'
        }

        id_change_query = text(f"UPDATE {TABLES[entity]} "
                               f"SET {COLUMNS[entity]} = '{body.correct_id}' "
                               f"WHERE {COLUMNS[entity]} = :id_to_change")
        for id_to_change in body.ids_to_change:
            db.execute(id_change_query, {'id_to_change': id_to_change})

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
        MODULES = {
            'institution': ('education', 'Institution'),
            'positions': ('Position'),
            'ranks': ('Rank'),
            'badges': ('Badge'),
            'penalties': ('Penalty'),
            'properties': ('additional', 'Properties'),
            'sports': ('personal', 'SportType'),
            'statuses': ('Status'),
            'specialties': ('education', 'Specialty'),
            'academic_degrees': ('education', 'AcademicDegreeDegree'),
            'academic_titles': ('education', 'AcademicTitleDegree'),
            'country': ('additional', 'Country'),
            'courses': ('education', 'Course'),
            'inst_degrees': ('education', 'InstitutionDegreeType'),
            'sciences': ('education', 'Science'),
            'languages': ('education', 'Language')
        }
        if len(MODULES[entity]) == 1:
            class_name = MODULES[entity]
            module = __import__('models',
                                fromlist=[class_name])
        else:
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
        current_obj.last_change = 'SOFT_UPDATE'
        current_obj.updated_at = datetime.now()

        db.add(new_obj)
        db.add(current_obj)
        db.flush()
        
        return new_obj.id

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
