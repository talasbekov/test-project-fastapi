"""migrate from oracle

Revision ID: f36891d5382e
Revises: 576296a7cdac
Create Date: 2023-06-05 18:17:57.957698

"""
import re
import uuid
import json
import logging
from datetime import datetime, timedelta
import importlib

import oracledb
from oracledb import Cursor
from alembic import op
from sqlalchemy import func
from sqlalchemy.orm import Session

from core import get_db, Base
from models import *
from utils import convert_days

oracledb.init_oracle_client()

log = logging.getLogger("root")

db = Session(bind=op.get_bind())


# revision identifiers, used by Alembic.
revision = "f36891d5382e"
down_revision = "3da03f49674d"
branch_labels = None
depends_on = None

division_context = {}
rank_context = {}

def get_uuid():
    return str(uuid.uuid4())


def extract_integers(string):
    pattern = r"\d+(?:\.\d+)?"
    matches = re.findall(pattern, string)
    floats = [float(match.replace(",", ".")) for match in matches]
    if len(floats) > 1:
        return floats[0] + (floats[1] * 0.1)
    elif len(floats) == 0:
        return 0
    return floats[0]


blood = {  # Группа Крови
    "0-ПОЛОЖИТЕЛЬНЫЙ": BloodType.O_PLUS,
    "0-ОТРИЦАТЕЛЬНЫЙ": BloodType.O_MINUS,
    "А-ПОЛОЖИТЕЛЬНЫЙ": BloodType.A_PLUS,
    "А-ОТРИЦАТЕЛЬНЫЙ": BloodType.A_MINUS,
    "В-ПОЛОЖИТЕЛЬНЫЙ": BloodType.B_PLUS,
    "В-ОТРИЦАТЕЛЬНЫЙ": BloodType.B_MINUS,
    "АВ-ПОЛОЖИТЕЛЬНЫЙ": BloodType.AB_PLUS,
    "АВ-ОТРИЦАТЕЛЬНЫЙ": BloodType.AB_MINUS,
}


def get_age_group(birthdate):
    years, _, _ = convert_days((datetime.now() - birthdate).days)
    if years <= 25 or years is None:
        return AgeGroup.FIRST
    elif years <= 30:
        return AgeGroup.SECOND
    elif years <= 35:
        return AgeGroup.THIRD
    elif years <= 40:
        return AgeGroup.FOURTH
    elif years <= 45:
        return AgeGroup.FIFTH
    return AgeGroup.SIXTH


counter = 1

new_contract_type = ContractType(
    id=get_uuid(),
    name="Контракт",
    nameKZ="Келісімшарт",
    years=0,
    is_finite=True,
)
db.add(new_contract_type)
db.flush()

def create_user(
    cursor: Cursor,
    db: Session,
    e_id,
    surname,
    name,
    father_name,
    officer_number,
    iin,
    family_status_name,
    service_id_number,
    service_id_end_date,
    fact_address,
    reg_address,
    gender,
    position_name,
    division_id,
    post_order_confirmer,
    post_order_number,
    post_order_date,
    birthdate,
    birth_place,
    nationality,
    blood_group,
    height,
    weight,
    hat_size,
    clothes_size,
    shoes_size,
    position_id,
    group_id,
    staff_unit_id,
    actual_staff_unit_id,
    status_id,
    rank_id,
):
    id = get_uuid()

    sql = f"""select  distinct(emp.id),concat(emp.IIN,'@sgo.kz')as email, FIRSTNAME, SURNAME,PATRONYMIC,pphone.phone_number as CALLSIGN,OFFICER_NUMBER, phone.PHONE_NUMBER, 'test address',
'doljnost', 'actual_doljnost', 1, 'supervised_id','description','cabinet',sphone.PHONE_NUMBER, 1,iin,emp.BIRTHDATE
from HR_EMPLOYEES emp 
left join HR_EMP_PHONES phone on phone.EMPLOYEE_ID = emp.ID and phone.PHONE_TYPE_ID= 2 
left join dic_hr_rank dr on dr.id = emp.RANK_ID 
left join HR_EMP_PHONES sphone on sphone.EMPLOYEE_ID = emp.ID and sphone.PHONE_TYPE_ID=3
left join HR_EMP_PHONES pphone on pphone.EMPLOYEE_ID = emp.ID and pphone.PHONE_TYPE_ID=15
        where emp.id = {e_id}"""

    (
        emp_id,
        email,
        name,
        surname,
        father_name,
        callsign,
        officer_number,
        phone_number,
        address,
        doljnost,
        actual_doljnost,
        is_active,
        supervised_id,
        description,
        cabinet,
        sphone,
        is_supervised,
        iin,
        birthdate,
    ) = cursor.execute(sql).fetchone()

    if status_id == 1:
        division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.CANDIDATES.value).first().id
        position_id = db.query(Position).filter(Position.name == PositionNameEnum.CANDIDATE.value).first().id
    elif status_id == 2 or status_id == 3:
        position_sql = f"""select cat.name_ru, dr.id,case when dp.name_ru like '%СГО%' or dp.name_ru like '%РК%' then dp.name_ru else initcap(dp.name_ru) end name_ru,
            case when dp.name_kz like '%МК%' then dp.name_kz else initcap(dp.name_kz) end name_kz, 
            ds.id
            from hr_division_structure ds
            left join hr_position_structure ps
                on ps.division_id = ds.id 
            left join hr_employees_easy_v v
                on (v.POSITION_ID = ps.id or v.POSITION_ID is null and v.INSTD_POSITION_ID = ps.id)
                and v.STATUS_CODE = 'ACTIVE'
            left join dic_hr_postname dp
                on dp.id = ps.position_id
                left join dic_hr_postname dp2
                on dp2.id = v.DIC_POSITION_ID
            left join dic_hr_postcategory dc
                on dc.id = ps.category_id
            left join dic_hr_rank dr
                on dr.id = ps.max_rank_id
                left join DIC_HR_POSTCATEGORY cat 
                    on cat.id = ps.category_id
            where ds.status = 3 and dr.id not in (1100038718,1100038503) and v.employee_id = {e_id}
        """

        position_res = cursor.execute(position_sql).fetchone()
        if position_res is None:
            return

        (
            category_name,
            pos_rank_id,
            my_position_name,
            my_position_name_kz,
            my_division_id
        ) = position_res

        division = db.query(StaffDivision).filter(StaffDivision.id == division_context.get(my_division_id)).first()
        if division is not None:
            division_id = division.id
        position = db.query(Position).filter(func.lower(Position.name) == my_position_name.lower()).first()
        if position is None:
            found_rank = db.query(Rank).filter(Rank.id == rank_context.get(pos_rank_id)).first()
            if found_rank is not None:
                pos_rank_id = found_rank.id
            else:
                pos_rank_id = None

            position_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_positions"],
                [{
                    "id": position_id,
                    'name': my_position_name,
                    'nameKZ': my_position_name_kz,
                    'max_rank_id': pos_rank_id,
                    'category_code': category_name,
                    'form': 'Форма 1'
                }]
            )
        else:
            position_id = position.id
    elif status_id == 5:
        division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.IN_RESERVE.value).first().id
        position_id = db.query(Position).filter(Position.name == PositionNameEnum.IN_RESERVE.value).first().id
    elif status_id == 7:
        division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.OUT_STAFF.value).first().id
        position_id = db.query(Position).filter(Position.name == PositionNameEnum.OUT_STAFF.value).first().id
    elif status_id == 8:
        division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.RETIRED.value).first().id
        position_id = db.query(Position).filter(Position.name == PositionNameEnum.RETIRED.value).first().id
    elif status_id == 9:
        division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.DEAD.value).first().id
        position_id = db.query(Position).filter(Position.name == PositionNameEnum.DEAD.value).first().id

    op.bulk_insert(
        Base.metadata.tables["hr_erp_staff_units"],
        [
            {
                "id": staff_unit_id,
                "user_id": id,
                "position_id": position_id,
                "staff_division_id": division_id,
                "user_replacing_id": None,
                "requirements": json.dumps([
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru",
                            },
                            {"text": ["Жоғары кәсіпкерлік"], "lang": "kz"},
                        ],
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": [
                                    "10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                    "4 года стажа работы на руководящих должностях",
                                ],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                    "4 жыл басшы лауазымдардағы жұмыс өтілі",
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": [
                                    "Наличие обязательных знаний, умений и навыков"
                                ],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Міндетті білімнің, іскерліктің және дағдылардың болуы"
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Денсаулық жағдайы бойынша жарамдылық"
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                ]),
            }
        ],
    )
    while (
        callsign is not None
        and db.query(User).filter(User.call_sign == callsign).first()
        is not None
    ):
        callsign = f"0{callsign}"

    found_rank = db.query(Rank).filter(Rank.id == rank_context.get(rank_id)).first()
    if found_rank is None:
        found_rank = db.query(Rank).filter(Rank.name == "Рядовой").first()
    op.bulk_insert(
        Base.metadata.tables["hr_erp_users"],
        [
            {
                "id": id,
                "email": email,
                "password": "$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m",
                "first_name": name,
                "last_name": surname,
                "father_name": father_name,
                "staff_unit_id": staff_unit_id,
                "date_birth": birthdate,
                "supervised_by": None,
                "call_sign": callsign,
                "id_number": officer_number,
                "phone_number": phone_number,
                "rank_id": str(found_rank.id),
                "actual_staff_unit_id": actual_staff_unit_id,
                "icon": f"https://10.15.3.180/s3/static/{iin}.jpg",
                "service_phone_number": sphone,
                "personal_id": emp_id,
                "is_military": True,
                "cabinet": cabinet,
                "address": address,
                "iin": iin,
                "is_active": is_active,
            }
        ],
    )

    profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_profiles"],
        [
            {
                "id": profile_id,
                "user_id": id,
            }
        ],
    )

    personal_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_personal_profiles"],
        [
            {
                "id": personal_profile_id,
                "profile_id": profile_id,
            }
        ],
    )

    educational_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_educational_profiles"],
        [{"id": educational_profile_id, "profile_id": profile_id}],
    )

    medical_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_medical_profiles"],
        [{"id": medical_profile_id, "profile_id": profile_id}],
    )

    additional_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_additional_profiles"],
        [{"id": additional_profile_id, "profile_id": profile_id}],
    )

    family_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_family_profiles"],
        [{"id": family_profile_id, "profile_id": profile_id}],
    )

    # Medical Profile

    general_user_information_id = get_uuid()

    blood_group_enum = blood.get(blood_group, None)

    op.bulk_insert(
        Base.metadata.tables["hr_erp_general_user_info"],
        [
            {
                "id": general_user_information_id,
                "height": int(float(extract_integers(height)))
                if height is not None
                else None,
                "blood_group": blood_group_enum.value
                if blood_group_enum is not None
                else None,
                "age_group": get_age_group(birthdate),
                "profile_id": medical_profile_id,
                "weight": int(float(extract_integers(weight)))
                if weight is not None
                else None,
            }
        ],
    )

    anthropometric_data_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_anthropometric_data"],
        [
            {
                "id": anthropometric_data_id,
                "head_circumference": int(
                    float(
                        extract_integers(hat_size.split("-")[0].split("/")[0])
                    )
                )
                if hat_size is not None
                else None,
                "shoe_size": int(
                    float(
                        extract_integers(
                            shoes_size.split("-")[0].split("/")[0]
                        )
                    )
                )
                if shoes_size is not None
                else None,
                "neck_circumference": 35,
                "shape_size": int(
                    float(
                        extract_integers(
                            clothes_size.split("-")[0].split("/")[0]
                        )
                    )
                )
                if clothes_size is not None
                else None,
                "bust_size": 56,
                "profile_id": medical_profile_id,
            }
        ],
    )

    # Personal Profile

    f_status = (
        db.query(FamilyStatus)
        .filter(
            func.lower(FamilyStatus.name).contains(family_status_name.lower())
        )
        .first()
    )

    biographic_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_biographic_infos"],
        [
            {
                "id": biographic_info_id,
                "place_birth": birth_place,
                "gender": gender,
                "citizenship": "Казахстан",
                "nationality": nationality,
                "family_status_id": str(f_status.id) if f_status else None,
                "address": reg_address,
                "residence_address": fact_address,
                "profile_id": personal_profile_id,
            }
        ],
    )

    tax_declaration1_id = get_uuid()
    tax_declaration2_id = get_uuid()
    tax_declaration3_id = get_uuid()
    tax_declaration4_id = get_uuid()
    tax_declaration5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_tax_declarations"],
        [
            {
                "id": tax_declaration1_id,
                "year": "2019",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration2_id,
                "year": "2020",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration3_id,
                "year": "2021",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration4_id,
                "year": "2022",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration5_id,
                "year": "2023",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
        ],
    )

    user_financial_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_user_financial_infos"],
        [
            {
                "id": user_financial_info_id,
                "iban": "KZ200155980950859874",
                "housing_payments_iban": "KZ200155980950859874",
                "profile_id": personal_profile_id,
            }
        ],
    )

    ids_sql = f"""select hecd.cert_document_type_id, hecd.doc_number, hecd.begin_date, hecd.end_date, dco.name_ru from HR_EMP_CERT_DOCUMENTS hecd 
         left join hr_employees emmp on emmp.id = hecd.employee_id left join DIC_CERT_ORGAN dco on dco.id = hecd.issue_organ_id where emmp.id = {emp_id} and hecd.cert_document_type_id in (1000000001, 1000000003, 1000000008) and hecd.end_date > sysdate order by hecd.cert_document_type_id"""

    ids = cursor.execute(ids_sql).fetchall()

    for personal_id in ids:
        (
            document_type_id,
            document_number,
            date_of_issue,
            date_to,
            issued_by,
        ) = personal_id

        if document_type_id == 1000000001:  # TODO: ID
            identification_card_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_identification_cards"],
                [
                    {
                        "id": identification_card_id,
                        "document_number": document_number,
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "issued_by": issued_by,
                        "document_link": "https://10.15.3.180/s3/static/example.txt",
                        "profile_id": personal_profile_id,
                    }
                ],
            )
        elif document_type_id == 1000000003:  # TODO: Passport
            passport_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_passports"],
                [
                    {
                        "id": passport_id,
                        "document_number": document_number,
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "issued_by": issued_by,
                        "document_link": "https://10.15.3.180/s3/static/example.txt",
                        "profile_id": personal_profile_id,
                    }
                ],
            )
        elif document_type_id == 1000000008:  # TODO: Driving License
            driving_sql = f"""select 
         case when auto_category_a = 1 then 'A,' else '' end || 
           case when auto_category_b = 1 then 'B,' else '' end || 
             case when auto_category_c=1 then 'C,' else '' end ||
               case when auto_category_d=1 then 'D,' else '' end || 
                 case when auto_category_e=1 then 'E' else '' end  as auto_category
                   from hr_employees where id = {emp_id}"""
            category_res = cursor.execute(driving_sql).fetchone()
            category = category_res[0]
            category_array = []
            if category is not None:
                category = "".join([i for i in category_res])
                if category[len(category) - 1] == ",":
                    category = category[: len(category) - 1]
                category_array = category.split(",")
            driving_licence_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_driving_licenses"],
                [
                    {
                        "id": driving_licence_id,
                        "document_number": document_number,
                        "category": json.dumps(category_array),
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "document_link": "https://10.15.3.180/s3/static/example.txt",
                        "profile_id": personal_profile_id,
                    }
                ],
            )

    # Sport Degrees and Achievements
    sport_degrees_sql = f"""SELECT
                                 INITCAP(dsr.NAME_ru) AS SPORT_RANK,
                                 INITCAP(dsk.NAME_ru) AS SPORT_KIND,
                                 INITCAP(dsr.NAME_KZ) AS sport_rank_kz,
                                 INITCAP(dsk.NAME_KZ) AS sport_kind_kz
                                 FROM HR_EMP_SPORTS s
                                 LEFT JOIN DIC_HR_SPORT_RANK dsr ON (dsr.ID = s.SPORT_RANK_ID)
                                 LEFT JOIN DIC_HR_SPORT_KIND dsk ON (dsk.ID = s.SPORT_KIND_ID)
                                 left join hr_employees emmp on emmp.id = s.EMPLOYEE_ID
                                 WHERE emmp.id = {emp_id}"""

    sport_degrees = cursor.execute(sport_degrees_sql).fetchall()
    for i in sport_degrees:
        sport_rank, sport_kind, sport_rank_kz, sport_kind_kz = i
        found_sport = (
            db.query(SportType)
            .filter(func.lower(SportType.name) == (sport_kind.lower()))
            .first()
        )
        if found_sport is None:
            found_sport_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_sport_types"],
                [
                    {
                        "id": found_sport_id,
                        "name": sport_kind,
                        "nameKZ": sport_kind_kz,
                    }
                ],
            )
        else:
            found_sport_id = found_sport.id
        op.bulk_insert(
            Base.metadata.tables["hr_erp_sport_degrees"],
            [
                {
                    "id": get_uuid(),
                    "profile_id": personal_profile_id,
                    "name": f"{sport_rank} {sport_kind}",
                    "nameKZ": f"{sport_rank_kz} {sport_kind_kz}",
                    "assignment_date": datetime.now(),
                    "document_link": "https://10.15.3.180/s3/static/example.txt",
                    "sport_type_id": str(found_sport_id),
                }
            ],
        )

    # Education Profile
    education_sql = f"""SELECT
                            'CE' AS EDU_TYPE,
                            ce.START_DATE,
                            ce.FINISH_DATE,
                            del.name_ru,
                            del.NAME_KZ,
                            INITCAP(ce.INSTITUTION_ru) AS INSTITUTION,
                            INITCAP(ce.INSTITUTION_KZ) as INSTITUTION_kz
                            FROM HR_EMP_CIVIL_EDUCATION ce
                            LEFT JOIN DIC_HR_EDUCATION_FORM def ON (def.ID = ce.EDUCATION_FORM_ID)
                            LEFT JOIN DIC_HR_EDUCATION_LEVEL del ON (del.ID = ce.EDUCATION_LEVEL_ID)
                            left join hr_employees emmp on emmp.id = ce.employee_id
                            WHERE del.CODE IN ('003', '004', '005') AND def.CODE IN ('001') AND emmp.ID = {emp_id}
                            UNION
                            SELECT
                            'ME',
                            me.START_DATE,
                            me.FINISH_DATE,
                            dmi.NAME_ru,
                            dmi.NAME_KZ,
                            INITCAP(del.name_ru),
                            INITCAP(del.NAME_KZ)
                            FROM HR_EMP_MILITARY_EDUCATION me
                            LEFT JOIN DIC_HR_MILITARY_INSTITUTION dmi ON (dmi.ID = me.MILITARY_INSTITUTION_ID)
                            LEFT JOIN DIC_HR_EDUCATION_FORM def ON (def.ID = me.EDUCATION_FORM_ID)
                            LEFT JOIN DIC_HR_EDUCATION_LEVEL del ON (del.ID = me.EDUCATION_LEVEL_ID)
                            left join hr_employees emmp on emmp.id = me.employee_id
                            WHERE del.CODE IN ('003', '004', '005') AND def.CODE IN ('001') AND emmp.ID = {emp_id}
                            ORDER BY START_DATE DESC"""

    educations = cursor.execute(education_sql).fetchall()

    for education in educations:
        (
            edu_type,
            start_date,
            end_date,
            nameRU,
            nameKZ,
            institutionRU,
            institutionKZ,
        ) = education
        institution = (
            db.query(Institution).filter(Institution.name == nameRU).first()
        )
        if institution is None:
            institution_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_institutions"],
                [
                    {
                        "id": institution_id,
                        "name": institutionRU,
                        "nameKZ": institutionKZ,
                    }
                ],
            )
        else:
            institution_id = institution.id
        education_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_educations"],
            [
                {
                    "id": education_id,
                    "profile_id": educational_profile_id,
                    "institution_id": str(institution_id),
                    "start_date": start_date,
                    "end_date": end_date,
                    "document_link": "https://10.15.3.180/s3/static/example.txt",
                }
            ],
        )

    courses_sql = f"""SELECT
                            c.BEGIN_DATE,
                            c.END_DATE,
                            NVL(INITCAP(dmi.NAME_ru), INITCAP(c.ORGANISATION_ru)) AS ORGANIZATION,
                            NVL(INITCAP(dmi.NAME_KZ), INITCAP(c.ORGANISATION_KZ)) as ORGANIZATION_KZ,
                            INITCAP(c.COURSE_NAME_ru) AS COURSE_NAME,
                            INITCAP(c.COURSE_NAME_KZ) AS COURSE_NAME_KZ
                            FROM HR_EMP_ADD_COURSES c
                            LEFT JOIN DIC_HR_MILITARY_INSTITUTION dmi ON (dmi.ID = c.MILITARY_INSTITUTION_ID)
                            LEFT JOIN DIC_HR_ADD_COURSE_TYPE dct ON (dct.ID = c.COURSES_TYPE_ID)
                            LEFT JOIN HR_EMPLOYEES emmp on c.EMPLOYEE_ID = emmp.ID
                            WHERE emmp.ID = {emp_id}
                            ORDER BY BEGIN_DATE"""

    courses = cursor.execute(courses_sql).fetchall()

    for course in courses:
        course_id = get_uuid()
        (
            start_date,
            end_date,
            organizationRU,
            organizationKZ,
            course_nameRU,
            course_nameKZ,
        ) = course
        if (
            organizationRU is None
            or organizationKZ is None
            or course_nameRU is None
            or course_nameKZ is None
        ):
            continue
        provider = (
            db.query(CourseProvider)
            .filter(func.lower(CourseProvider.name) == organizationRU.lower())
            .first()
        )
        if provider is None:
            course_provider_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_course_providers"],
                [
                    {
                        "id": course_provider_id,
                        "name": organizationRU,
                        "nameKZ": organizationKZ,
                    }
                ],
            )
        else:
            course_provider_id = provider.id
        op.bulk_insert(
            Base.metadata.tables["hr_erp_courses"],
            [
                {
                    "id": course_id,
                    "profile_id": educational_profile_id,
                    "course_provider_id": str(course_provider_id),
                    "name": course_nameRU,
                    "nameKZ": course_nameKZ,
                    "start_date": start_date,
                    "end_date": end_date,
                    "document_link": "https://10.15.3.180/s3/static/example.txt",
                }
            ],
        )

    # Language Proficiencies
    language_proficiencies_sql = f"""SELECT
                                 INITCAP(dl.NAME_ru) AS LANG_NAME,
                                 INITCAP(dl.NAME_KZ) as lang_name_kz,
                                 INITCAP(dlk.NAME_ru) AS LANG_LEVEL,
                                 INITCAP(dlk.NAME_KZ) as lang_level_kz
                                 FROM HR_EMP_LANGUAGES l
                                 LEFT JOIN DIC_HR_LANGUAGES dl ON (dl.ID = l.LANGUAGE_ID)
                                 LEFT JOIN DIC_HR_LANGUAGE_LEVEL_KNOWS dlk ON (dlk.ID = l.LEVEL_KNOWS_ID)
                                 LEFT JOIN HR_EMPLOYEES emmp on emmp.id = l.employee_id
                                 where emmp.id = {emp_id}"""

    languages = cursor.execute(language_proficiencies_sql).fetchall()

    for lang in languages:
        (lang_name, lang_name_kz, lang_level, lang_level_kz) = lang
        found_lang = (
            db.query(Language)
            .filter(func.lower(Language.name).contains(lang_name.lower()))
            .first()
        )
        if found_lang is None:
            found_lang = Language(
                id=get_uuid(),
                name=lang_name,
                nameKZ=lang_name_kz,
            )
            db.add(found_lang)
        language_proficiency_id = get_uuid()
        proficiency_in_lang = LanguageProficiency(
            id=language_proficiency_id,
            profile_id=educational_profile_id,
            language_id=str(found_lang.id),
            level=5,
        )
        db.add(proficiency_in_lang)

    # Academic Degrees
    # TODO: add scientific degrees
    # Academic Title
    # TODO: add scientific titles

    # Vehicles
    vehicles_sql = f"""select (INITCAP(br.NAME_RU) || ' ' || t.TRANSPORT_MODEL) as nameRU, (INITCAP(br.NAME_KZ)|| ' ' || t.TRANSPORT_MODEL) as nameKZ, NVL(ISSUE_YEAR, 1970), TRANSPORT_NUMBER from HR_EMP_TRANSPORTS t
    left join DIC_TRANSPORT_BRAND br on br.id = t.TRANSPORT_BRAND_ID
    left join hr_employees emp on t.EMPLOYEE_ID = emp.ID
    where emp.ID = {emp_id}"""

    vehicles = cursor.execute(vehicles_sql).fetchall()

    for vehicle in vehicles:
        (nameRU, nameKZ, issue_date, vehicle_number) = vehicle
        issue_date = datetime(year=issue_date, month=1, day=1)
        vehicle_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_user_vehicles"],
            [
                {
                    "id": vehicle_id,
                    "profile_id": additional_profile_id,
                    "vin_code": "JN1WNYD21U0000001",
                    "date_from": issue_date,
                    "number": vehicle_number,
                    "name": nameRU,
                    "nameKZ": nameKZ,
                    "document_link": "https://10.15.3.180/s3/static/example.txt",
                }
            ],
        )

    # Family Profile
    family_sql = f"""select INITCAP(rs.name_ru), INITCAP(rs.name_kz), r.surname,r.firstname, r.patronymic, r.iin, r.BIRTHDATE, r.DEADDATE,
       INITCAP(dc.NAME_ru)|| ' '||lower(te1.NAME_ru)||' '||INITCAP(r.BIRTHPLACE_TE1_ru)||' '||lower(te2.NAME_ru)||' '||INITCAP(r.BIRTHPLACE_TE2_RU)||' '||lower(dst.NAME_ru)||' '||INITCAP(r.BIRTHPLACE_SETTLEMENT_ru) as birthplace,
       ADDRESS_RU,
       workplace_ru from HR_EMP_RELATIVES r
left join hr_employees emp on emp.id = r.employee_id
LEFT JOIN DIC_COUNTRY dc ON (dc.ID = r.CITIZENSHIP_ID)
LEFT JOIN DIC_TE1_TYPE te1 ON (te1.ID = r.BIRTHPLACE_TE1_TYPE_ID)
LEFT JOIN DIC_TE2_TYPE te2 ON (te2.ID = r.BIRTHPLACE_TE2_TYPE_ID)
LEFT JOIN DIC_SETTLEMENT_TYPE dst ON (dst.ID = r.BIRTHPLACE_SETTLEMENT_TYPE_ID)
left join DIC_HR_RELATIVE_STATUS rs on rs.id = r.relative_status_id
where emp.ID = {emp_id}"""

    families = cursor.execute(family_sql).fetchall()

    for family_member in families:
        (
            relative_status,
            relative_status_kz,
            surname,
            firstname,
            patronymic,
            iin,
            birthdate,
            deathdate,
            birthplace,
            address,
            workplace,
        ) = family_member

        if birthplace is not None:
            birthplace = " ".join(birthplace.split(" "))
        if address is not None:
            address = " ".join(address.split(" "))
        if workplace is not None:
            workplace = " ".join(workplace.split(" "))

        relation = (
            db.query(FamilyRelation)
            .filter(func.lower(FamilyRelation.name) == relative_status.lower())
            .first()
        )
        if relation is None:
            relation = FamilyRelation(
                id=get_uuid(), name=relative_status, nameKZ=relative_status_kz
            )
            db.add(relation)
        family_member_id = get_uuid()
        db.add(
            Family(
                id=family_member_id,
                profile_id=family_profile_id,
                first_name=firstname,
                last_name=surname,
                father_name=patronymic,
                birthday=birthdate,
                death_day=deathdate,
                birthplace=birthplace if birthplace is not None else "",
                address=address if address is not None else "",
                workplace=workplace if workplace is not None else "",
                relation_id=str(relation.id),
                IIN=iin,
            )
        )
    # Service Profile

    badge_sql = f"""SELECT
                    (SELECT dhat.NAME_ru FROM dic_hr_award_type dhat WHERE dhat.ID = t.AWARD_NAME_ID) AWARD_NAME,
                    (SELECT dhat.NAME_kz FROM dic_hr_award_type dhat WHERE dhat.ID = t.AWARD_NAME_ID) AWARD_NAME_KZ,
                    t.DOC_NUMBER,
                    t.DOC_DATE
                    FROM hr_emp_awards t where t.employee_id = {emp_id} order by t.DOC_DATE"""

    badges = cursor.execute(badge_sql).fetchall()

    for i in badges:
        (
            award_name,
            award_nameKZ,
            doc_number,
            doc_date,
        ) = i
        found_badge_type = (
            db.query(BadgeType)
            .filter(func.lower(BadgeType.name) == award_name.lower())
            .first()
        )
        if found_badge_type is None:
            found_badge_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_badge_types"],
                [
                    {
                        "id": found_badge_type_id,
                        "name": award_name,
                        "nameKZ": award_nameKZ,
                        "url": "https://10.15.3.180/s3/static/example.txt",
                    }
                ],
            )
        else:
            found_badge_type_id = found_badge_type.id
        badge_id = get_uuid()
        new_badge = Badge(
            id=badge_id,
            user_id=id,
            type_id=str(found_badge_type_id),
        )
        db.add(new_badge)
        new_badge_history = BadgeHistory(
            date_from=doc_date,
            date_to=None,
            user_id=id,
            date_credited=doc_date,
            document_number=doc_number,
            badge_id=str(badge_id),
        )
        db.add(new_badge_history)

    penalty_sql = f"""SELECT
                (SELECT pt.NAME_ru FROM dic_hr_penalty_type pt WHERE pt.ID = t.PENALTY_TYPE_ID) PENALTY_TYPE, 
                (SELECT pt.NAME_kz FROM dic_hr_penalty_type pt WHERE pt.ID = t.PENALTY_TYPE_ID) PENALTY_TYPE_KZ, 
                t.ORDER_BEGIN_NUMBER, 
                t.ORDER_BEGIN_DATE, 
                t.ORDER_END_NUMBER, 
                t.ORDER_END_DATE
                FROM hr_emp_penalty t 
                WHERE t.EMPLOYEE_ID = {emp_id} order by t.ORDER_BEGIN_DATE"""

    penalties = cursor.execute(penalty_sql).fetchall()

    for i in penalties:
        (
            penalty_name,
            penalty_nameKZ,
            pen_number,
            date_from,
            pen_end_number,
            date_to,
        ) = i
        found_penalty_type = (
            db.query(PenaltyType)
            .filter(func.lower(PenaltyType.name) == penalty_name.lower())
            .first()
        )
        if found_penalty_type is None:
            found_penalty_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_penalty_types"],
                [
                    {
                        "id": found_penalty_type_id,
                        "name": penalty_name,
                        "nameKZ": penalty_nameKZ,
                    }
                ],
            )
        else:
            found_penalty_type_id = found_penalty_type.id
        new_penalty = Penalty(
            id=get_uuid(),
            type_id=str(found_penalty_type_id),
            user_id=id,
        )
        db.add(new_penalty)
        if date_to is not None:
            date_to = date_to
        elif date_from is None:
            date_to = None
        else:
            date_to = date_from + timedelta(weeks=25)
        new_penalty_history = PenaltyHistory(
            id=get_uuid(),
            date_from=date_from,
            document_number=pen_number,
            date_credited=date_from,
            date_to=date_to,
            penalty_id=str(new_penalty.id),
        )
        db.add(new_penalty_history)

    attestation_sql = f"""SELECT
                t.ATTESTATION_DATE,
                t.CONCLUSION_KZ,
                t.CONCLUSION_RU
                FROM hr_emp_attestation t where t.employee_id = {emp_id} order by t.attestation_date"""

    attestations = cursor.execute(attestation_sql).fetchall()

    for i in attestations:
        (date_from, conclusionKZ, conclusion) = i
        new_attestation = Attestation(id=get_uuid(), user_id=id)
        db.add(new_attestation)
        new_history = AttestationHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_from + timedelta(weeks=156),
            date_credited=date_from,
            attestation_id=str(new_attestation.id),
            attestation_status=conclusion,
        )
        db.add(new_history)

    emergency_service_sql = f"""select * from (select * from (SELECT t.BEGIN_DATE,t.END_DATE, case
                           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                                nvl(t.instead_of_post_id, 0) = 0 and
                                nvl(t.dic_post_instd_id, 0) = 0 and
                                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
                            t.post_ru
                           when nvl(t.instead_of_post_id, 0) <> 0 then
                            (select dhp.name_ru
                               from dic_hr_postname dhp
                              where dhp.id = t.dic_post_instd_id)
                           when nvl(t.post_id, 0) <> 0 then
                            (select dhp.name_ru
                               from hr_position_structure hps
                               join dic_hr_postname dhp
                                 on dhp.id = hps.position_id
                              where hps.id = t.post_id)
                           when nvl(t.dic_post_instd_id, 0) <> 0 then
                            (select dhp.name_ru
                               from dic_hr_postname dhp
                              where dhp.id = t.dic_post_instd_id)
                           when exists (select 1
                                   from dic_hr_order_type dhot
                                  where dhot.id = t.order_begin_type_id
                                    and dhot.code in ('002', '006', '008')) then
                            (select yn.name_ru
                               from dic_adm_yes_no yn
                              where yn.code = 'AT_COMMAND')
                           else
                            null
                         end as position_ru,
                         
                         case
                           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                                nvl(t.instead_of_post_id, 0) = 0 and
                                nvl(t.dic_post_instd_id, 0) = 0 and
                                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
                            t.post_kz
                           when nvl(t.instead_of_post_id, 0) <> 0 then
                            (select dhp.name_kz
                               from dic_hr_postname dhp
                              where dhp.id = t.dic_post_instd_id)
                           when nvl(t.post_id, 0) <> 0 then
                            (select dhp.name_kz
                               from hr_position_structure hps
                               join dic_hr_postname dhp
                                 on dhp.id = hps.position_id
                              where hps.id = t.post_id)
                           when nvl(t.dic_post_instd_id, 0) <> 0 then
                            (select dhp.name_kz
                               from dic_hr_postname dhp
                              where dhp.id = t.dic_post_instd_id)
                           when exists (select 1
                                   from dic_hr_order_type dhot
                                  where dhot.id = t.order_begin_type_id
                                    and dhot.code in ('002', '006', '008')) then
                            (select yn.name_kz
                               from dic_adm_yes_no yn
                              where yn.code = 'AT_COMMAND')
                           else
                            null
                         end as position_kz,
 (select nvl(sum(pct_value),0) from hr_emp_soprecord_pcts where soprecord_id =t.id) as percent,
                               1.5 as koef,
                               case when 
                 nvl(t.division_id, 0) = 0 AND nvl(t.post_id, 0) = 0 AND nvl(t.instead_of_post_id, 0) = 0 then t.division_ru 
                 else
                 (select full_name_ru from HR_DIVISION_STRUCTURE str where t.division_id = str.id) 
                 end as div_full_name, 
                 
                t.ORDER_BEGIN_NUMBER, 
                t.ORDER_BEGIN_DATE, 
                t.ORDER_END_NUMBER, 
                t.ORDER_END_DATE, 
                t.ORDER_END_CONFIRMER_ru END_CONFIRMER 
                 FROM hr_emp_soprecords_v t WHERE t.EMPLOYEE_ID = {emp_id} order by t.begin_date, t.id)
                union
                select * from (SELECT  
                t.BEGIN_DATE, 
                t.END_DATE, 
                t.POSITION_RU, 
                t.POSITION_KZ, 
                0 as percent,
                (SELECT dhac.COEFF_VALUE FROM dic_hr_advantage_coeff dhac WHERE dhac.ID = t.ADVANTAGE_COEFF_ID) KOEF,
                (SELECT dhmso.NAME_ru FROM dic_hr_milit_serv_organization dhmso WHERE dhmso.ID = t.MILIT_SERV_ORG_ID) div_full_name, 
                '' as order_begin_number,
                t.BEGIN_DATE as ORDER_BEGIN_DATE,
                '' as order_end_number,
                t.END_DATE as ORDER_END_DATE,
                '' as end_confirmer                
                FROM hr_emp_milrecords t where t.EMPLOYEE_ID = {emp_id} order by t.begin_date)) order by begin_date
"""

    emergency_services = cursor.execute(emergency_service_sql).fetchall()

    for i in emergency_services:
        (
            begin_date,
            end_date,
            position_name,
            position_nameKZ,
            percent,
            coeff,
            division_name,
            doc_number,
            doc_date,
            doc_end_number,
            doc_end_date,
            confirmer,
        ) = i
        found_position = (
            db.query(Position)
            .filter(func.lower(Position.name) == position_name)
            .first()
        )
        new_history = EmergencyServiceHistory(
            id=get_uuid(),
            date_from=begin_date,
            date_to=end_date,
            user_id=id,
            document_number=doc_number,
            date_credited=begin_date,
            coefficient=coeff,
            percentage=percent,
            staff_division_name=division_name,
            staff_division_nameKZ=division_name,
            contractor_signer_name=confirmer,
            contractor_signer_nameKZ=confirmer,
        )
        if found_position is None:
            new_history.name = position_name
            new_history.nameKZ = position_nameKZ
        else:
            new_history.position_id = found_position.id
        db.add(new_history)

    # Work Experience
    work_experience_sql = f"""
    select BEGIN_DATE, END_DATE, ORGANIZATION_RU, POSITION_RU, IS_USED from HR_EMP_WORKRECORDS
    WHERE EMPLOYEE_ID = {emp_id}
    """
    
    work_experiences = cursor.execute(work_experience_sql).fetchall()
    
    for i in work_experiences:
        (
            date_from,
            date_to,
            org_name,
            pos_name,
            is_credited,
        ) = i
        
        new_work_experience = WorkExperienceHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=id,
            name_of_organization=org_name,
            position_work_experience=pos_name,
            is_credited=is_credited,
        )
        
        db.add(new_work_experience)

    secondments_sql = f"""select t.begin_date,t.end_date, t.div_name_ru division, t.div_name_kz
                from HR_EMP_ATTACHMENTS_V t where t.employee_id = {emp_id}"""
    
    secondments = cursor.execute(secondments_sql).fetchall()
    for i in secondments:
        (
            date_from,
            date_to,
            div_name,
            div_nameKZ,
        ) = i
        
        new_secondment = Secondment(
            id=get_uuid(),
            name=div_name,
            nameKZ=div_nameKZ,
            staff_division_id=None,
            state_body_id =None,
            user_id = id
        )
        db.add(new_secondment)
        new_secondment_history = SecondmentHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_to,
            secondment_id=new_secondment.id,
        )
        db.add(new_secondment_history)

    # Service IDS
    service_id_sql = f"""select oc_number, oc_begin_date, oc_end_date, token from HR_EMPLOYEES
    where ID = {emp_id}"""
    
    service_ids = cursor.execute(service_id_sql).fetchall()
    for i in service_ids:
        (
            number,
            date_from,
            date_to,
            token
        ) = i
        ServiceID(
            id=get_uuid(),
            number=number,
            date_to=date_to,
            token_status=ServiceIDStatus.RECEIVED,
            id_status=ServiceIDStatus.RECEIVED,
            user_id=id
        )
    # Leaves
    leave_sql = f"""select l.leave_type_id, l.begin_date, l.end_date, l.order_number, l.order_date, l.order_confirmer_ru, l.order_confirmer_kz,t.name_ru, t.name_kz
from HR_EMP_LEAVES l
left join dic_hr_leave_type t on t.id = l.leave_type_id 
where l.employee_id = {emp_id}

union
select 0,rl.begin_date,rl.end_date,rl.report_order_number,rl.report_date, rl.report_order_confirmer_ru,rl.report_order_confirmer_kz, 'Ежегодный отпуск', 'Жыл сайынғы демалыс' from HR_EMP_REGLEAVES rl
where rl.employee_id = {emp_id}
"""
    leaves = cursor.execute(leave_sql).fetchall()
    
    for i in leaves:
        (
            leave_type_id,
            date_from,
            date_to,
            order_number,
            order_date,
            confirmer,
            confirmerKZ,
            nameRU,
            nameKZ,
        ) = i
        new_status = Status(
            id=get_uuid(),
            user_id=id,
        )
        db.add(new_status)
        new_status_history = StatusHistory(
            id=get_uuid(),
            status_name=nameRU,
            status_id=new_status.id,
            document_number=order_number
        )
        db.add(new_status_history)

    # Contracts
    contract_sql = f"""select * from (SELECT
                (SELECT dayn.NAME_ru FROM dic_adm_yes_no dayn WHERE dayn.YES_NO_TYPE = 'D' AND dayn.TRUTH_VALUE = t.UNDER_LIMIT_AGE) UNDER_LIMIT_NAME, 
                (SELECT dayn.NAME_ru FROM dic_adm_yes_no dayn WHERE dayn.YES_NO_TYPE = 'D' AND dayn.TRUTH_VALUE = t.OVER_LIMIT_AGE) OVER_LIMIT_NAME, 
                t.UNDER_LIMIT_AGE, 
                t.OVER_LIMIT_AGE, 
                t.BEGIN_DATE, 
                t.END_DATE, 
                floor(months_between(t.end_date,t.begin_date)/12) as years,
                t.ORDER_NUMBER, 
                t.ORDER_DATE, 
                t.ORDER_CONFIRMER_KZ, 
                t.ORDER_CONFIRMER_RU
                 FROM hr_emp_contracts t where t.employee_id = {emp_id})where years > 0
"""
    contracts = cursor.execute(contract_sql).fetchall()

    for i in contracts:
        (
            under_limit_name,
            over_limit_name,
            under_limit_age,
            over_limit_age,
            date_from,
            date_to,
            years,
            doc_number,
            doc_date,
            confirmerKZ,
            confirmer,
        ) = i

        new_contract = Contract(
            id=get_uuid(),
            type_id=new_contract_type.id,
            user_id=id,
        )
        db.add(new_contract)

        new_contract_history = ContractHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_to,
            contract_id=new_contract.id,
            experience_years=years,
            document_number=doc_number,
        )
        db.add(new_contract_history)
        
    db.flush()


def upgrade() -> None:
    conn = oracledb.connect(
        user="admin_sop", password="welcome1", dsn="10.15.3.31/SOPPROD"
    )
    cursor: Cursor = conn.cursor()

    db = Session(bind=op.get_bind())

    rank_sql = """select id, name_ru, name_kz from dic_hr_rank"""
    
    for i in cursor.execute(rank_sql).fetchall():
        (
            rank_id,
            rank_name,
            rank_nameKZ,
        ) = i
        new_rank_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_ranks"],
            [{
                "id": new_rank_id,
                'name': rank_name,
                'nameKZ': rank_nameKZ,
            }]
        )
        rank_context[rank_id] = new_rank_id


    division_sql = """select id, case when parent_id = 0 then null else parent_id end, name_ru,name_kz
    from hr_division_structure where status = 3 order by tree_level"""

    for i in cursor.execute(division_sql).fetchall():
        (
            id,
            parent_id,
            name,
            nameKZ
        ) = i
        new_division_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_staff_divisions"],
            [{
                'id': new_division_id,
                'name': name,
                'nameKZ': nameKZ,
                'parent_group_id': division_context.get(parent_id, None),
                'is_combat_unit': True,
                'description': '',
                'leader_id': None
            }]
        )
        division_context[id] = new_division_id

    special_group = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.SPECIAL_GROUP).first()
    for i in special_group.children:
        division_context[i.id] = i.id

    overall_sql = f"""select e.ID,
    e.SURNAME,
    e.FIRSTNAME,
    e.PATRONYMIC,
    e.OFFICER_NUMBER,
    e.IIN,
    dfs.name_ru,
    e.oc_number as securityId,e.oc_end_date securityId_endDate,
    (select 
                 ADDRESS_SETTLEMENT_ru || ', ' || ADDRESS_GEONIM_ru || ' ' || ADDRESS_HOUSE || ', ' || ADDRESS_FLAT as address
                 from hr_emp_addresses where employee_id = e.id and address_type_id = 1000000002 and rownum = 1) as fact_address,
    (select ADDRESS_SETTLEMENT_ru || ', ' || ADDRESS_GEONIM_ru || ' ' || ADDRESS_HOUSE || ', ' || ADDRESS_FLAT as address
                from hr_emp_addresses where employee_id = e.id and address_type_id = 1000000001 and rownum = 1) as reg_address,
    case when oc.sex_name_ru='МУЖСКОЙ' then 1 else 0 end as gender,
    
    NVL(dpn.NAME_ru, sr.POST_ru) AS POST_NAME,
    sr.division_id,
    sr.ORDER_BEGIN_CONFIRMER_ru AS POST_ORDER_CONFIRMER,
--         case
--             when oc.POSITION_NAME_RU like '%аспоряж%'
--                 then (select dhrp.name_short_ru as POST_ORDER_CONFIRMER_POST from hr_position_structure hrps
--                                                                                       left join dic_hr_postname dhrp on dhrp.id = hrps.position_id
--                       where hrps.id = (select post_id from (select sop.post_id, row_number() over (order by sop.id desc)as rn from  HR_EMP_SOPRECORDS sop where employee_id = (select order_approver_id from hr_order_caption where id = sr.ORDER_BEGIN_ID) ) where rn = 2 ))
--             else oc.POSITION_NAME_ru
--             end as POST_ORDER_CONFIRMER_POST,
    sr.ORDER_BEGIN_NUMBER AS POST_ORDER_NUMBER,
    sr.ORDER_BEGIN_DATE AS POST_ORDER_DATE,
    e.BIRTHDATE,
    INITCAP(dc.NAME_ru)||' '||lower(te1.NAME_ru)|| ' '||INITCAP(e.BIRTH_TE1_ru)||' '||lower(te2.NAME_ru)||' '||INITCAP(e.BIRTH_TE2_ru)||' '||lower(dst.NAME_ru)||' '||INITCAP(e.BIRTH_SETTLEMENT_ru) as birthplace,
    case
        when e.sex_id = 1000000001 then INITCAP(dn.NAME_ru)
        else INITCAP(dn.f_name_ru) end AS NATIONALITY_NAME,
    concat(concat(dbg.NAME_ru,'-'), drf.name_ru) AS BLOOD_GROUP,
    e.HEIGHT,
    e.WEIGHT,
    e.SIZE_OF_HAT,
    e.CLOTHING_SIZE,
    e.SHOES_SIZE,
    e.status_id,
    vvv.rank_id
FROM HR_EMPLOYEES e
         LEFT JOIN HR_EMP_SOPRECORDS sr ON (sr.EMPLOYEE_ID = e.ID AND sr.IS_ACTIV = 1)
         LEFT JOIN HR_EMPLOYEES_EASY_V vvv on vvv.EMPLOYEE_ID = e.id
         LEFT JOIN HR_DIVISION_STRUCTURE ds ON (TO_NUMBER(ds.ID) = NVL2(sr.ID, sr.DIVISION_ID, TO_NUMBER(e.DIVISION_ID)))
         LEFT JOIN HR_POSITION_STRUCTURE ps ON (TO_NUMBER(ps.ID) = sr.POST_ID)
         LEFT JOIN DIC_HR_POSTNAME dpn ON (dpn.ID = NVL(ps.POSITION_ID, sr.DIC_POST_INSTD_ID))
         LEFT JOIN DIC_COUNTRY dc ON (dc.ID = e.BIRTH_COUNTRY_ID)
         LEFT JOIN DIC_TE1_TYPE te1 ON (te1.ID = e.BIRTH_TE1_TYPE_ID)
         LEFT JOIN DIC_TE2_TYPE te2 ON (te2.ID = e.BIRTH_TE2_TYPE_ID)
         LEFT JOIN DIC_SETTLEMENT_TYPE dst ON (dst.ID = e.BIRTH_SETTLEMENT_TYPE_ID)
         LEFT JOIN DIC_NATIONALITY dn ON (dn.ID = e.NATIONALITY_ID)
         LEFT JOIN DIC_BLOOD_GROUP dbg ON (dbg.ID = e.BLOOD_GROUP_ID)
         LEFT JOIN DIC_RHESUS_FACTOR drf ON (drf.ID = e.RHESUS_FACTOR_ID)
         LEFT JOIN HR_ORDER_CAPTION o ON (o.ID = sr.ORDER_BEGIN_ID)
         LEFT JOIN HR_EMPLOYEES_EASY_V oc ON (oc.EMPLOYEE_ID = o.ORDER_APPROVER_ID)
         left join DIC_FAMILY_STATUS dfs on dfs.id = e.family_status_id
         left join hr_emp_status hes on hes.id = e.status_id
         where hes.id in (1,2,3,5,7,8,9)"""

    found_position = db.query(Position).first()
    found_division = (
        db.query(StaffDivision)
        .filter(StaffDivision.name == StaffDivisionEnum.SPECIAL_GROUP.value)
        .first()
    )

    for row in cursor.execute(overall_sql).fetchall():
        (
            e_id,
            surname,
            name,
            father_name,
            officer_number,
            iin,
            family_status_name,
            service_id_number,
            service_id_end_date,
            fact_address,
            reg_address,
            gender,
            position_name,
            division_id,
            post_order_confirmer,
            post_order_number,
            post_order_date,
            birthdate,
            birth_place,
            nationality,
            blood_group,
            height,
            weight,
            hat_size,
            clothes_size,
            shoes_size,
            status_id,
            rank_id
        ) = row
        staff_unit_id = get_uuid()
        create_user(
            cursor,
            db,
            e_id,
            surname,
            name,
            father_name,
            officer_number,
            iin,
            family_status_name,
            service_id_number,
            service_id_end_date,
            fact_address,
            reg_address,
            gender,
            position_name,
            division_id,
            post_order_confirmer,
            post_order_number,
            post_order_date,
            birthdate,
            birth_place,
            nationality,
            blood_group,
            height,
            weight,
            hat_size,
            clothes_size,
            shoes_size,
            found_position.id,
            found_division.id,
            staff_unit_id,
            staff_unit_id,
            status_id,
            rank_id,
        )


def downgrade() -> None:
    pass
