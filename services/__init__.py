# Be careful of imports order is important!
# Possible problems are circular imports, partial initialization of module
from .base import ServiceBase
from .profile import *

from .jurisdiction import jurisdiction_service
from .staff_division import staff_division_service
from .service_staff_function_type import service_staff_function_type_service
from .document_staff_function_type import document_staff_function_type_service
from .service_staff_function import service_staff_function_service
from .hr_document_step import hr_document_step_service
from .document_staff_function import document_staff_function_service

from .staff_unit import staff_unit_service

from .badge import badge_service
from .equipment import equipment_service
from .event import event_service
from .rank import rank_service
from .jurisdiction import jurisdiction_service
from .user_stat import user_stat_service

from .staff_division import staff_division_service

from .hr_document_template import hr_document_template_service

from .user import user_service
from .auth import auth_service
from .hr_document_info import hr_document_info_service
from .hr_document import hr_document_service
from .staff_list import staff_list_service

from .additional import *
from .education import *
from .family import *
from .archive import *
