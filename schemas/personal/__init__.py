from .family_status import FamilyStatusCreate, FamilyStatusRead, FamilyStatusUpdate
from .city import CityCreate, CityRead, CityUpdate
from .region import RegionCreate, RegionRead, RegionUpdate
from .citizenship import (CitizenshipCreate, CitizenshipRead, CitizenshipUpdate)
from .nationality import (NationalityCreate, NationalityRead, NationalityUpdate)
from .birthplace import (BirthplaceCreate, BirthplaceRead, BirthplaceUpdate)
from .biographic_info import (BiographicInfoCreate, BiographicInfoRead,
                              BiographicInfoUpdate)
from .driving_license import (DrivingLicenseCreate, DrivingLicenseRead,
                              DrivingLicenseUpdate, DrivingLicenseLinkUpdate)
from .identification_card import (IdentificationCardCreate,
                                  IdentificationCardRead,
                                  IdentificationCardUpdate)
from .passport import PassportCreate, PassportRead, PassportUpdate
from .sport_type import (SportTypeCreate, SportTypeUpdate, SportTypeRead,
                         SportTypePaginationRead)
from .sport_achievement import (SportAchievementCreate, SportAchievementRead,
                                SportAchievementUpdate)
from .sport_degree import SportDegreeCreate, SportDegreeRead, SportDegreeUpdate
from .tax_declaration import (TaxDeclarationCreate, TaxDeclarationRead,
                              TaxDeclarationUpdate)
from .user_financial_info import (UserFinancialInfoCreate,
                                  UserFinancialInfoRead,
                                  UserFinancialInfoUpdate)
from .personal_profile import (PersonalProfileCreate, PersonalProfileRead,
                               PersonalProfileUpdate)
from .sport_degree_type import *


