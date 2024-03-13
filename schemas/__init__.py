from .base import Model, NamedModel, ReadModel, ReadNamedModel, ReadTextModel, TextModel
from .badge import *
from .autotag import *
from .equipment import (EquipmentCreate,
                        EquipmentRead,
                        EquipmentUpdate,
                        TypeClothingEquipmentRead,
                        TypeArmyEquipmentRead,
                        TypeOtherEquipmentRead,
                        TypeArmyEquipmentReadPagination,
                        TypeClothingEquipmentReadPagination,
                        TypeOtherEquipmentReadPagination,
                        TypeArmyEquipmentCreate,
                        TypeArmyEquipmentModelCreate,
                        TypeClothingEquipmentCreate,
                        TypeClothingEquipmentModelCreate,
                        TypeOtherEquipmentCreate,
                        TypeOtherEquipmentModelCreate,
                        )

from .event import EventCreate, EventRead, EventUpdate
from .hr_document_template import (HrDocumentTemplateCreate,
                                   HrDocumentTemplateRead,
                                   HrDocumentTemplateUpdate,
                                   SuggestCorrections,
                                   HrDocumentTemplatePaginationRead)
from .permission import (PermissionCreate, PermissionRead, PermissionUpdate,
                         UserPermission, PermissionTypeRead, PermissionType,
                         PermissionPaginationRead)

from .rank import RankCreate, RankRead, RankUpdate, RankPaginationRead
from .position import PositionCreate, PositionUpdate, PositionRead, PositionPaginationRead, PositionReadShort, PositionTypeRead, PositionTypeUpdate
from .jurisdiction import JurisdictionRead, JurisdictionCreate, JurisdictionUpdate
from .staff_function_type import (DocumentStaffFunctionTypeCreate, DocumentStaffFunctionTypeRead,
                                  DocumentStaffFunctionTypeUpdate, ServiceStaffFunctionTypeCreate,
                                  ServiceStaffFunctionTypeRead, ServiceStaffFunctionTypeUpdate)
from .staff_function import (DocumentStaffFunctionCreate, DocumentStaffFunctionRead, DocumentStaffFunctionUpdate,
                             ServiceStaffFunctionCreate, ServiceStaffFunctionRead, ServiceStaffFunctionUpdate,
                             StaffUnitFunctions, StaffFunctionRead, DocumentStaffFunctionAdd,
                             DocumentStaffFunctionConstructorAdd, DocumentStaffFunctionAppendToStaffUnit, StaffUnitFunctionsByPosition)
from .status import *
from .staff_division_type import (
    StaffDivisionTypeBase,
    StaffDivisionTypeCreate,
    StaffDivisionTypeRead,
    StaffDivisionTypeUpdate)
from .staff_division import (StaffDivisionCreate, StaffDivisionRead, StaffDivisionReadMinimized, StaffDivisionChildReadMinimized, StaffDivisionBaseMinimized,
                             StaffDivisionStepRead, StaffDivisionUpdate, StaffDivisionChildReadSchedule, StaffDivisionReadSchedule, StaffDivisionBaseSchedule, StaffUnitReadSchedule, UserReadSchedule,
                             StaffDivisionUpdateParentGroup,
                             StaffDivisionOptionRead, StaffUnitDivisionRead,
                             StaffDivisionReadWithoutStaffUnit,
                             StaffDivisionVacancyRead, StaffUnitMatreshkaOptionRead,
                             StaffUnitMatreshkaOptionReadPagination,
                             ShortStaffUnitDivisionRead, StaffDivisionOptionChildRead,
                             StaffDivisionMatreshkaStepRead, StaffDivisionNamedModel, StaffDivisionTreeRead, StaffDivisionChildReadScheduleShort, StaffDivisionReadScheduleShort)
from .staff_unit import (StaffUnitCreate, StaffUnitRead, StaffUnitUpdate,
                         UserStaffUnitRead, StaffUnitCreateWithPosition,
                         ShortUserStaffUnitRead, StaffUnitFromArchiveCreate, StaffUnitUpdateOverwrite)
from .state_body import StateBodyCreate, StateBodyRead, StateBodyUpdate
from .hr_document_step import (HrDocumentStepCreate, HrDocumentStepRead,
                               HrDocumentStepUpdate)

from .user import (UserCreate, UserRead, UserUpdate,
                   UserGroupUpdate, UserShortRead,
                   UserShortReadStatus, TableUserRead,
                   UserShortReadStatusPagination,
                   UserShortReadAgeCategory,
                   UserShortReadPagination, UserShortReadFullNames)
from .profile import ProfileCreate, ProfileUpdate, ProfileRead
from .hr_document_status import HrDocumentStatusRead, HrDocumentStatusCreate, HrDocumentStatusUpdate
from .hr_document import (HrDocumentCreate, HrDocumentInit, HrDocumentRead,
                          HrDocumentSign, HrDocumentUpdate, DraftHrDocumentCreate,
                          DraftHrDocumentInit, HrDocumentInitEcp, HrDocumentSignEcp, HrDocumentSignEcpWithIds,
                          QrRead)
from .hr_document_info import (HrDocumentInfoCreate, HrDocumentInfoRead,
                               HrDocumentInfoUpdate, HrDocumentHistoryRead)
from .privelege_emergency import (
    PrivelegeEmergencyCreate,
    PrivelegeEmergencyRead,
    PrivelegeEmergencyUpdate)
from .personnal_reserve import (
    PersonnalReserveCreate,
    PersonnalReserveRead,
    PersonnalReserveUpdate)
from .coolness import *
from .user_stat import UserStatCreate, UserStatRead, UserStatUpdate
from .auth import LoginForm, RegistrationForm, CandidateRegistrationForm, EcpLoginForm
from .staff_list import (
    StaffListCreate,
    StaffListRead,
    StaffListUpdate,
    StaffListUserCreate,
    StaffListStatusRead,
    StaffListApplyRead)
from .service_id import (ServiceIDCreate, ServiceIDRead, ServiceIDUpdate)
from .military_unit import (
    MilitaryUnitCreate,
    MilitaryUnitRead,
    MilitaryUnitUpdate,
    MilitaryUnitReadPagination,)
from .user_oath import (UserOathCreate, UserOathRead, UserOathUpdate)
from .recommender_user import (
    RecommenderUserCreate,
    RecommenderUserRead,
    RecommenderUserUpdate)
from .additional import *
from .education import *
from .personal import *
from .medical import *
from .family import *
from .hr_vacancy_requirements import *
from .hr_vacancy_candidate import *
from .hr_vacancy import *
from .archive import *
from .user_candidates import *
from .penalty import *
from .contract import *
from .secondment import *
from .history import *
from .survey import *
from .bsp import *
from .notification import *
from .timeline import *
# from .hexagon import *
from .dictionaries import *
