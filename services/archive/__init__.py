from sqlalchemy.orm import Session
from models import StaffList

def increment_changes_size(db: Session, staff_list: StaffList):
    staff_list.changes_size += 1
    db.add(staff_list)


# Compilation of all services
from .service_archive_staff_function import service_archive_staff_function_service
from .document_archive_staff_function import document_archive_staff_function_service
from .service_archive_staff_function_type import service_archive_staff_function_type_service
from .document_archive_staff_function_type import document_archive_staff_function_type_service
from .archive_staff_division import archive_staff_division_service
from .archive_staff_function import archive_staff_function_service

from .archive_staff_unit import archive_staff_unit_service
