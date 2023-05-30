# Be careful of imports order is important!
# Possible problems are circular imports, partial initialization of module
from .base import ServiceBase
from .position import position_service
from .profile import *
from .notification import notification_service

from .jurisdiction import jurisdiction_service
from .staff_division import staff_division_service
from .service_staff_function_type import service_staff_function_type_service
from .document_staff_function_type import document_staff_function_type_service
from .service_staff_function import service_staff_function_service
from .hr_document_step import hr_document_step_service
from .document_staff_function import document_staff_function_service
from .archive import *
from .staff_unit import staff_unit_service

from .badge import badge_service
from .equipment import equipment_service
from .event import event_service
from .rank import rank_service
from .user_stat import user_stat_service

from .staff_division import staff_division_service
from .category import categories, BaseCategory
from .recommender_user import recommender_user_service
from .hr_document_template import hr_document_template_service
from .personnal_reserve import personnal_reserve_service
from .hr_document_info import hr_document_info_service
from .hr_document_status import hr_document_status_service
from .user import user_service
from .status import status_service
from .status_leave import status_leave_service
from .secondment import secondment_service
from .privelege_emergency import privelege_emergency_service
from .coolness import coolness_service
from .penalty import penalty_service
from .contract import contract_service
from .service_id import service_id_service
from .military_unit import military_unit_service
from .user_oath import user_oath_service
from .history import *
from .staff_list import staff_list_service
from .hr_document import hr_document_service
from .additional import *
from .education import *
from .medical import *
from .family import *

from .candidates import *
from .render import render_service
from .auth import auth_service

from .hr_vacancy import hr_vacancy_service
from .hr_vacancy_requirements import hr_vacancy_requirement_service
