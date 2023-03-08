from .profile import ProfileCreate, ProfileUpdate, ProfileRead
from .personal import (PersonalProfileCreate, PersonalProfileUpdate, PersonalProfileRead,
                       BiographicInfoCreate, BiographicInfoUpdate, BiographicInfoRead,
                       DrivingLicenceCreate, DrivingLicenceUpdate, DrivingLicenceRead,
                       IdentificationCardCreate, IdentificationCardUpdate, IdentificationCardRead,
                       PassportRead, PassportUpdate, PassportCreate,
                       SportAchievementUpdate, SportAchievementRead, SportAchievementCreate,
                       SportDegreeRead, SportDegreeUpdate, SportDegreeCreate,
                       TaxDeclarationRead, TaxDeclarationUpdate, TaxDeclarationCreate,
                       UserFinancialInfoRead, UserFinancialInfoUpdate, UserFinancialInfoCreate)
from .badge import BadgeCreate, BadgeRead, BadgeUpdate
from .equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate
from .jurisdiction import JurisdictionRead, JurisdictionCreate, JurisdictionUpdate
from .event import EventCreate, EventRead, EventUpdate
from .hr_document_template import (HrDocumentTemplateCreate,
                                   HrDocumentTemplateRead,
                                   HrDocumentTemplateUpdate)
from .permission import (PermissionCreate, PermissionRead, PermissionUpdate,
                         UserPermission)
from .rank import RankCreate, RankRead, RankUpdate
from .position import PositionCreate, PositionUpdate, PositionRead
from .staff_function_type import (DocumentStaffFunctionTypeCreate, DocumentStaffFunctionTypeRead,
                                  DocumentStaffFunctionTypeUpdate, ServiceStaffFunctionTypeCreate,
                                  ServiceStaffFunctionTypeRead, ServiceStaffFunctionTypeUpdate)
from .staff_function import (DocumentStaffFunctionCreate, DocumentStaffFunctionRead, DocumentStaffFunctionUpdate,
                             ServiceStaffFunctionCreate, ServiceStaffFunctionRead, ServiceStaffFunctionUpdate,
                             StaffUnitFunctions, StaffFunctionRead, DocumentStaffFunctionAdd)
from .staff_division import (StaffDivisionCreate, StaffDivisionRead,
                             StaffDivisionUpdate, StaffDivisionUpdateParentGroup, StaffDivisionOptionRead)
from .staff_unit import StaffUnitCreate, StaffUnitRead, StaffUnitUpdate
from .hr_document_step import (HrDocumentStepCreate, HrDocumentStepRead,
                               HrDocumentStepUpdate)
from .user import UserCreate, UserRead, UserUpdate, UserGroupUpdate
from .hr_document import (HrDocumentCreate, HrDocumentInit, HrDocumentRead,
                          HrDocumentSign, HrDocumentUpdate)

from .hr_document_info import (HrDocumentInfoCreate, HrDocumentInfoRead,
                               HrDocumentInfoUpdate, HrDocumentHistoryRead)
from .user_stat import UserStatCreate, UserStatRead, UserStatUpdate
from .auth import LoginForm, RegistrationForm
from .additional import *

