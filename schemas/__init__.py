from .auth import LoginForm, RegistrationForm
from .badge import BadgeCreate, BadgeRead, BadgeUpdate
from .equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate
from .event import EventCreate, EventRead, EventUpdate
from .hr_document_template import (HrDocumentTemplateCreate,
                                   HrDocumentTemplateRead,
                                   HrDocumentTemplateUpdate)
from .hr_document import (HrDocumentCreate, HrDocumentInit, HrDocumentRead,
                          HrDocumentSign, HrDocumentUpdate)
from .permission import (PermissionCreate, PermissionRead, PermissionUpdate,
                         UserPermission)
from .rank import RankCreate, RankRead, RankUpdate
from .staff_function import StaffFunctionCreate, StaffFunctionRead, StaffFunctionUpdate
from .staff_division import (StaffDivisionCreate, StaffDivisionRead,
                             StaffDivisionUpdate)
from .staff_unit import StaffUnitCreate, StaffUnitRead, StaffUnitUpdate
from .hr_document_step import (HrDocumentStepCreate, HrDocumentStepRead,
                               HrDocumentStepUpdate)
from .user import UserCreate, UserRead, UserUpdate
from .hr_document_info import (HrDocumentInfoCreate, HrDocumentInfoRead,
                               HrDocumentInfoUpdate, HrDocumentHistoryRead)
from .user_stat import UserStatCreate, UserStatRead, UserStatUpdate
