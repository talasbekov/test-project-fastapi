from .base import Model, NamedModel, ReadModel, ReadNamedModel
from .badge import *
from .equipment import (EquipmentCreate, 
                        EquipmentRead, 
                        EquipmentUpdate,
                        TypeClothingEquipmentRead, 
                        TypeArmyEquipmentRead, 
                        TypeOtherEquipmentRead
                    )

from .event import EventCreate, EventRead, EventUpdate
from .hr_document_template import (HrDocumentTemplateCreate,
                                   HrDocumentTemplateRead,
                                   HrDocumentTemplateUpdate)
from .permission import (PermissionCreate, PermissionRead, PermissionUpdate,
                         UserPermission)

from .rank import RankCreate, RankRead, RankUpdate
from .position import PositionCreate, PositionUpdate, PositionRead
from .jurisdiction import JurisdictionRead, JurisdictionCreate, JurisdictionUpdate
from .staff_function_type import (DocumentStaffFunctionTypeCreate, DocumentStaffFunctionTypeRead,
                                  DocumentStaffFunctionTypeUpdate, ServiceStaffFunctionTypeCreate,
                                  ServiceStaffFunctionTypeRead, ServiceStaffFunctionTypeUpdate)
from .staff_function import (DocumentStaffFunctionCreate, DocumentStaffFunctionRead, DocumentStaffFunctionUpdate,
                             ServiceStaffFunctionCreate, ServiceStaffFunctionRead, ServiceStaffFunctionUpdate,
                             StaffUnitFunctions, StaffFunctionRead, DocumentStaffFunctionAdd,
                             DocumentStaffFunctionConstructorAdd)
from .staff_division import (StaffDivisionCreate, StaffDivisionRead,
                             StaffDivisionUpdate, StaffDivisionUpdateParentGroup,
                             StaffDivisionOptionRead, StaffUnitDivisionRead)
from .staff_unit import StaffUnitCreate, StaffUnitRead, StaffUnitUpdate, UserStaffUnitRead
from .hr_document_step import (HrDocumentStepCreate, HrDocumentStepRead,
                               HrDocumentStepUpdate)
from .status import *
from .user import UserCreate, UserRead, UserUpdate, UserGroupUpdate
from .profile import ProfileCreate, ProfileUpdate, ProfileRead
from .hr_document_status import HrDocumentStatusRead, HrDocumentStatusCreate, HrDocumentStatusUpdate
from .hr_document import (HrDocumentCreate, HrDocumentInit, HrDocumentRead,
                          HrDocumentSign, HrDocumentUpdate, DraftHrDocumentCreate,
                          DraftHrDocumentInit)
from .hr_document_info import (HrDocumentInfoCreate, HrDocumentInfoRead,
                               HrDocumentInfoUpdate, HrDocumentHistoryRead)
from .privelege_emergency import (PrivelegeEmergencyCreate, PrivelegeEmergencyRead, PrivelegeEmergencyUpdate)
from .personnal_reserve import (PersonnalReserveCreate, PersonnalReserveRead, PersonnalReserveUpdate)
from .coolness import *
from .user_stat import UserStatCreate, UserStatRead, UserStatUpdate
from .auth import LoginForm, RegistrationForm, CandidateRegistrationForm
from .staff_list import (StaffListCreate, StaffListRead, StaffListUpdate, StaffListUserCreate)
from .service_id import (ServiceIDCreate, ServiceIDRead, ServiceIDUpdate)
from .military_unit import (MilitaryUnitCreate, MilitaryUnitRead, MilitaryUnitUpdate)
from .user_oath import (UserOathCreate, UserOathRead, UserOathUpdate)
from .recommender_user import (RecommenderUserCreate, RecommenderUserRead, RecommenderUserUpdate)
from .additional import *
from .education import *
from .personal import *
from .medical import *
from .family import *
from .archive import *
from .user_candidates import *
from .penalty import *
from .contract import *
from .secondment import *
from .history import *
