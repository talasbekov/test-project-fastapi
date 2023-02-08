# Be careful of imports order is important!
# Possible problems are circular imports, partial initialization of module

from .hr_document import hr_document_service
# Keep in mind that I have hr_document_service in this file
# So I need to make sure that it will initialize before initializing my file
from .hr_document_template import hr_document_template_service
from .group import group_service
from .hr_document_info import hr_document_info_service
from .hr_document_step import hr_document_step_service
from .role import role_service
from .user_stat import user_stat_service
from .position import position_service
from .permission import permission_service
from .user import user_service
from .auth import auth_service
from .event import event_service
from .equipment import equipment_service
