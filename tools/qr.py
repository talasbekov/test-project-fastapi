import cx_Oracle
from names import generate_names, generate_phone_number, addresses, random_dates, ad, add, adf
from uuid import uuid4
from datetime import timedelta, datetime
import random
from enum import Enum

def convert_lob_to_str(obj):
    if isinstance(obj, cx_Oracle.LOB):
        return obj.read()
    elif isinstance(obj, dict):
        return {k: convert_lob_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_lob_to_str(elem) for elem in obj]
    else:
        return obj

academic_degrees_degrees = [
    '473d5627-47d3-48ec-8d10-7f4a24a641b8',
'4fc84352-b2c0-46f6-9b4f-5d3df1058b27',
'f7c1c17f-c717-4936-83de-5fcbca7769df',
'f44805ab-38f8-4092-84bf-932842899c2f'
]




sciences_ids = [
    '15d67e17-7687-4f32-8e55-8ce0d987efc6',
'd852ba68-5296-462b-9c5d-804ecb9ac13d',
'4c2059fb-1acc-4c16-91f9-f87296ad7a9c',
'4ec08ed8-aaa5-4850-9c32-9a93a3360ec5',
'2eb56e62-748b-4ca7-8dde-0d77d1e82131',
'bf1e2404-9ee3-4335-8b0b-8df03790263b',
'74fbb51d-54fa-42c5-9f07-08950ee2e004',
'bc4f5704-07d4-44a5-84a2-47b75c7dff62',
'13112f42-9add-40be-a81d-466b182aeb0b',

]

class BloodType(str, Enum):
    O_PLUS = "O (I) Rh+"
    O_MINUS = "O (I) Rh-"
    A_PLUS = "A (II) Rh+"
    A_MINUS = "A (II) Rh-"
    B_PLUS = "B (III) Rh+"
    B_MINUS = "B (III) Rh-"
    AB_PLUS = "AB (IV) Rh+"
    AB_MINUS = "AB (IV) Rh-"


def generate_code():
    return f"{random.randint(100000, 999999)}"

SQLALCHEMY_DATABASE_URL = f"oracle://system:Oracle123@172.20.0.2:1521/MORAL"
# Create a connection to the Oracle database
dsn_tns = cx_Oracle.makedsn('172.20.0.9', '1521', service_name='MORAL')
conn = cx_Oracle.connect(user='system', password='Oracle123', dsn=dsn_tns)

password = "$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m"
icon = "http://192.168.0.169:8083/static/placeholder.jpg"

# Create a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("SELECT * FROM HR_ERP_RANKS")
ranks = cursor.fetchall()
ranks = [convert_lob_to_str(rank) for rank in ranks]

# Close the cursor
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_SPECIALTIES")
specialties = cursor.fetchall()
specialties = [convert_lob_to_str(specialty) for specialty in specialties]
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_POSITIONS")
positions = cursor.fetchall()
positions = [convert_lob_to_str(position) for position in positions]
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_STAFF_DIVISIONS")
divisions = cursor.fetchall()
divisions = [division for division in divisions]
cursor.close()

cursor = conn.cursor()

cursor.execute("SELECT * FROM HR_ERP_BADGE_TYPES")
badge_types = cursor.fetchall()
badge_types = [convert_lob_to_str(badge_type) for badge_type in badge_types]
cursor.close()


cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_COURSE_PROVIDERS")
course_providers = cursor.fetchall()
course_providers = [convert_lob_to_str(course_provider) for course_provider in course_providers]
cursor.close()


cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_INSTITUTIONS")
institutions = cursor.fetchall()
institutions = [convert_lob_to_str(institution) for institution in institutions]
cursor.close()


cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_LANGUAGES")
languages = cursor.fetchall()
languages = [convert_lob_to_str(language) for language in languages]
cursor.close()


cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_SPORT_TYPES")
sport_types = cursor.fetchall()
sport_types = [convert_lob_to_str(sport_type) for sport_type in sport_types]
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_SPORT_DEGREE_TYPES")
sport_degree_types = cursor.fetchall()
sport_degree_types = [convert_lob_to_str(sport_degree_type) for sport_degree_type in sport_degree_types]
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT * FROM HR_ERP_COUNTRIES")
countries_db = cursor.fetchall()
countries_db = [convert_lob_to_str(country) for country in countries_db]
cursor.close()




 

# Execute the SQL query
names = generate_names(ad, add, adf, 10000)




counter = 0
for name in names:
    new_id = str(uuid4())
    first_name = name[0]
    last_name = name[1]
    father_name= name[2]

    email = f"user_{counter}@mail.ru"
    phone_number = generate_phone_number()
    call_sign = str(random.choice(["Альфа", "Бетта", "Гамма"]) + ' ' + str(random.randint(0, 999999999)))
    counter += 1

    id_number = str(random.randint(1000000000, 9999999999))
    address = random.choice(addresses)
    rank_id = random.choice(ranks)[5] 
    last_signed_at = None
    date_birth = random.choice(random_dates)
    iin = "".join([str(random.randint(0, 9)) for _ in range(12)])
    is_active = True
    cabinet = f"{random.randint(1, 9)}.{random.randint(1, 99)}.{random.randint(1, 999)}K"
    personal_id = f"{random.randint(1000000000, 9999999999)}"
    service_phone_number = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(111, 999)}"
    is_military = random.choice([0, 1])
    

    # staff_unit create
    staff_unit_id = str(uuid4())
    is_active = 1
    user_replacing_id = None
    actual_position = random.choice(positions)[3]
    print(actual_position)
    position = random.choice(positions)[3]

    curator_of_id = None
    staff_division = random.choice(divisions)[6]
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO HR_ERP_STAFF_UNITS (POSITION_ID, STAFF_DIVISION_ID, USER_REPLACING_ID, ID, CURATOR_OF_ID, IS_ACTIVE, CREATED_AT, UPDATED_AT, REQUIREMENTS, TRIAL257, ACTUAL_POSITION_ID) VALUES ('{position}', '{staff_division}', null, '{staff_unit_id}', null, '{is_active}', SYSDATE, SYSDATE, null, null, '{actual_position}')") 
    cursor.close()
    # example of cabinet: 1.2.217K random
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO HR_ERP_USERS (EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, FATHER_NAME, CALL_SIGN, ID_NUMBER, PHONE_NUMBER, ADDRESS, RANK_ID, STAFF_UNIT_ID, ACTUAL_STAFF_UNIT_ID, IS_ACTIVE, SUPERVISED_BY, CABINET, SERVICE_PHONE_NUMBER, IS_MILITARY, PERSONAL_ID, IIN, DATE_BIRTH, ID, LAST_SIGNED_AT, CREATED_AT, UPDATED_AT, TRIAL346, DESCRIPTION, ICON) VALUES ('{email}', '{password}', '{first_name}', '{last_name}', '{father_name}', '{call_sign}', '{id_number}', '{phone_number}', '{address}', '{rank_id}', '{staff_unit_id}', '{staff_unit_id}', '{is_active}', null, '{cabinet}', '{service_phone_number}', '{is_military}', '{personal_id}', '{iin}', TO_DATE('{date_birth}', 'YYYY-MM-DD'), '{new_id}', null, SYSDATE, SYSDATE, null, null, '{icon}')") 
    cursor.close()

    cursor = conn.cursor()
    badge_id = str(uuid4())
    badges_len = len(badge_types)
    badge_type = random.choice(badge_types)
    
    print(badge_type)
    for i in random.sample(range(badges_len), random.randint(0, badges_len)):
        badge_new_id = str(uuid4())
        cursor.execute(f"INSERT INTO HR_ERP_BADGES (TYPE_ID, USER_ID, ID, CREATED_AT, UPDATED_AT, TRIAL774) VALUES ('{badge_type[1]}', '{new_id}', '{badge_new_id}', SYSDATE, SYSDATE, null)") 
    cursor.close()


    cursor = conn.cursor()
    profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_PROFILES (USER_ID, ID, CREATED_AT, UPDATED_AT, TRIAL117) VALUES ('{new_id}', '{profile_id}', SYSDATE, SYSDATE, null)") 
    cursor.close()


    
    cursor = conn.cursor()
    medical_profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_MEDICAL_PROFILES (PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{profile_id}', '{medical_profile_id}', SYSDATE, SYSDATE)")
    cursor.close()


    cursor = conn.cursor()
    educational_profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_EDUCATIONAL_PROFILES (PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{profile_id}', '{educational_profile_id}', SYSDATE, SYSDATE)")
    cursor.close()


    cursor = conn.cursor()
    personal_profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_PERSONAL_PROFILES (PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{profile_id}', '{personal_profile_id}', SYSDATE, SYSDATE)")
    cursor.close()


    cursor = conn.cursor()
    family_profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_FAMILY_PROFILES (PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{profile_id}', '{family_profile_id}', SYSDATE, SYSDATE)")
    cursor.close()

    cursor = conn.cursor()
    additional_profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_ADDITIONAL_PROFILES (PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{profile_id}', '{additional_profile_id}', SYSDATE, SYSDATE)")
    cursor.close()

    # get all family relations
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HR_ERP_FAMILY_RELATIONS")
    family_relations = cursor.fetchall()
    family_relations = [convert_lob_to_str(family_relation) for family_relation in family_relations]
    cursor.close()
    

    cursor = conn.cursor()
    family_id = str(uuid4())
    family_numbers = random.randint(0, 5)
    
    for family_number in range(family_numbers):
        print(1) 
        relation_id = random.choice(family_relations)[2]
        family_new_id = str(uuid4())
        family_first_name = random.choice(ad)
        family_last_name = random.choice(add)
        family_father_name = random.choice(adf)
        family_birthday = random.choice(random_dates)
        family_birthplace = random.choice(addresses)
        family_address = random.choice(addresses)
        family_workplace = random.choice(addresses)
        family_iin = "".join([str(random.randint(0, 9)) for _ in range(12)])
        cursor.execute(f"INSERT INTO HR_ERP_FAMILIES (FIRST_NAME, LAST_NAME, FATHER_NAME, IIN, BIRTHDAY, BIRTHPLACE, ADDRESS, WORKPLACE, RELATION_ID, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{family_first_name}', '{family_last_name}', '{family_father_name}', '{family_iin}', TO_DATE('{family_birthday}', 'YYYY-MM-DD'), '{family_birthplace}', '{family_address}', '{family_workplace}', '{relation_id}', '{family_profile_id}', '{family_new_id}', SYSDATE, SYSDATE)")
    cursor.close()


    cursor = conn.cursor()
    hospital_data = random.randint(0, 5)
    for hospital in range(hospital_data):
        # medical
        reasons = [
            {
                "name" : "По причине болезни",
                "namekz" : "Денсаулығыма байланысты"
            },
            {
                "name" : "По причине травмы",
                "namekz" : "Теріске байланысты"
            },
            {
                "name" : "Сломал ногу",
                "namekz" : "Аяғымды сындырып алдым"
            },
            {
                "name" : "По причине травмы",
                "namekz" : "Аяғыма байланысты"
            }
        ]

        reason = random.choice(reasons)
        reason_kz = reason["namekz"]
        reason = reason["name"]

        places = [
            {
                "name" : "Городская больница",
                "namekz" : "Қала ауруханасы"
            },
            {
                "name" : "Областная больница",
                "namekz" : "Аймақ ауруханасы"
            },
            {
                "name" : "Районная больница",
                "namekz" : "Аудан ауруханасы"
            },
            {
                "name" : "Поликлиника",
                "namekz" : "Поликлиника"
            }
        ]

        place = random.choice(places)
        place_kz = place["namekz"]
        place = place["name"]
        start_date = random.choice(random_dates)
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d') 
            
        hospital_data_id = str(uuid4())
        cursor.execute(f"INSERT INTO HR_ERP_HOSPITAL_DATAS (CODE, REASON, REASONKZ, PLACE, PLACEKZ, START_DATE, END_DATE, DOCUMENT_LINK, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{generate_code()}', '{reason}', '{reason_kz}', '{place}', '{place_kz}', TO_DATE('{start_date}', 'YYYY-MM-DD'), TO_DATE('{end_date}', 'YYYY-MM-DD'), null, '{medical_profile_id}', '{hospital_data_id}', SYSDATE, SYSDATE)")
    
    cursor.close()


    is_check = random.choice([0, 1])
    if is_check == 1:            
        cursor = conn.cursor()
        anthropometric_data_id = str(uuid4())
        head_circumference = random.randint(40, 60)
        shoe_size = random.randint(30, 50)
        neck_circumference = random.randint(20, 40)
        shape_size = random.randint(30, 50)
        bust_size = random.randint(30, 50)
        cursor.execute(f"INSERT INTO HR_ERP_ANTHROPOMETRIC_DATA (HEAD_CIRCUMFERENCE, SHOE_SIZE, NECK_CIRCUMFERENCE, SHAPE_SIZE, BUST_SIZE, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{head_circumference}', '{shoe_size}', '{neck_circumference}', '{shape_size}', '{bust_size}', '{medical_profile_id}', '{anthropometric_data_id}', SYSDATE, SYSDATE)")
        cursor.close()

    """
    INITIATOR
START_DATE
END_DATE
DOCUMENT_LINK
PROFILE_ID
NAME
NAMEKZ
ID
CREATED_AT
UPDATED_AT
TRIAL866
INITIATORKZ
    """
    cursor = conn.cursor()
    dispency = random.randint(0, 5)
    for number in range(dispency):
            
        dispensary_registration_id = str(uuid4())
        initiator = random.choice(names)
        initiator_kz = random.choice(names)
        start_date = random.choice(random_dates)
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')

        initiator = initiator[0] + " " + initiator[1] + " " + initiator[2] if initiator[2] else initiator[0] + " " + initiator[1]
        initiator_kz = initiator_kz[0] + " " + initiator_kz[1] + " " + initiator_kz[2] if initiator_kz[2] else initiator_kz[0] + " " + initiator_kz[1]

        cursor.execute(f"INSERT INTO HR_ERP_DISP_REGISTRATIONS (INITIATOR, INITIATORKZ, START_DATE, END_DATE, DOCUMENT_LINK, PROFILE_ID, NAME, NAMEKZ, ID, CREATED_AT, UPDATED_AT, TRIAL866) VALUES ('{initiator}', '{initiator_kz}', TO_DATE('{start_date}', 'YYYY-MM-DD'), TO_DATE('{end_date}', 'YYYY-MM-DD'), null, '{medical_profile_id}', '{initiator}', '{initiator_kz}', '{dispensary_registration_id}', SYSDATE, SYSDATE, null)")
    cursor.close()



    is_check = random.choice([0, 1])
    if is_check == 1:
            
        cursor = conn.cursor()
        general_profile_id = str(uuid4())
        height = random.randint(150, 200)
        weight = random.randint(50, 150)
        blood_group = random.choice([BloodType.O_PLUS.value, BloodType.O_MINUS.value, BloodType.A_PLUS.value, BloodType.A_MINUS.value, BloodType.B_PLUS.value, BloodType.B_MINUS.value, BloodType.AB_PLUS.value, BloodType.AB_MINUS.value])
        age_group = random.choice([1, 2, 3, 4, 5, 6])
        cursor.execute(f"INSERT INTO HR_ERP_GENERAL_USER_INFO (HEIGHT, WEIGHT, BLOOD_GROUP, AGE_GROUP, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{height}', '{weight}', '{blood_group}', '{age_group}', '{medical_profile_id}', '{general_profile_id}', SYSDATE, SYSDATE)")
        cursor.close()

    cursor = conn.cursor()
    
    user_liberation_id = str(uuid4())
    # get all liberations
    
     
    reasons = ["Отпуск", "Уход за ребенком"]
    reasons_kz = ["Татым", "Баланы қамтиту"]

    cursor.execute("SELECT * FROM HR_ERP_LIBERATIONS")
    liberations = cursor.fetchall()
    liberations = [convert_lob_to_str(liberation) for liberation in liberations]
    cursor.close()

    start_date = random.choice(random_dates)
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO HR_ERP_USER_LIBERATIONS (REASON, REASONKZ, INITIATOR, INITIATORKZ, START_DATE, END_DATE, DOCUMENT_LINK, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{random.choice(reasons)}', '{random.choice(reasons_kz)}', '{first_name}', '{last_name}', TO_DATE('{start_date}', 'YYYY-MM-DD'), TO_DATE('{end_date}', 'YYYY-MM-DD'), null, '{medical_profile_id}', '{user_liberation_id}', SYSDATE, SYSDATE)")
    cursor.close()

    cursor = conn.cursor()
    document_number = str(random.randint(100000, 999999))
    date_of_issue = random.choice(random_dates)
    date_to = (datetime.strptime(date_of_issue, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    issued_by = random.choice(["МВД", "МИД"])
    udo_id = str(uuid4())
    
    cursor.execute(f"INSERT INTO HR_ERP_PASSPORTS (DOCUMENT_NUMBER, DATE_OF_ISSUE, DATE_TO, ISSUED_BY, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{document_number}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), TO_DATE('{date_to}', 'YYYY-MM-DD'), '{issued_by}', '{personal_profile_id}', '{udo_id}', SYSDATE, SYSDATE)")
    cursor.close()


     
    cursor = conn.cursor()
    biographic_info_id = str(uuid4())
    place_birth = random.choice(address)
    gender = random.choice([0, 1])
    countries = ["Казахстан", "Россия", "Кыргызстан", "Таджикистан", "Узбекистан", "Туркменистан"]
    citizenship = random.choice(countries)
    nationalities = ["Казах", "Русский", "Кыргыз", "Таджик", "Узбек", "Туркмен"]
    nationality = random.choice(nationalities)
    countries_kz = ["Қазақстан", "Ресей", "Қырғызстан", "Тәжікстан", "Өзбекстан", "Түрікменстан"]
    citizenshipKZ = countries_kz[countries.index(citizenship)]
    nationalities_kz = ["Қазақ", "Орыс", "Қырғыз", "Тәжік", "Өзбек", "Түрік"]
    nationalityKZ = nationalities_kz[nationalities.index(nationality)]

    address = random.choice(addresses)


    # get all family statuses
    
    cursor.execute("SELECT * FROM HR_ERP_FAMILY_STATUSES")
    family_statuses = cursor.fetchall()
    family_statuses = [convert_lob_to_str(family_status) for family_status in family_statuses]
    cursor.close()
    
    cursor = conn.cursor()
    print(random.choice(family_statuses))
    family_status_id = random.choice(family_statuses)[2]

    cursor = conn.cursor()
    residence_address = random.choice(addresses)
    cursor.execute(f"INSERT INTO HR_ERP_BIOGRAPHIC_INFOS (PLACE_BIRTH, GENDER, CITIZENSHIP, NATIONALITY, CITIZENSHIPKZ, NATIONALITYKZ, ADDRESS, FAMILY_STATUS_ID, RESIDENCE_ADDRESS, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{place_birth}', '{gender}', '{citizenship}', '{nationality}', '{citizenshipKZ}', '{nationalityKZ}', '{address}', '{family_status_id}', '{residence_address}', '{personal_profile_id}', '{biographic_info_id}', SYSDATE, SYSDATE)")
    cursor.close()
    

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):                
            cursor = conn.cursor()
            degree_id = random.choice(academic_degrees_degrees)
            science_id = random.choice(sciences_ids)
            specialty_id = random.choice(specialties)[2]
            document_number = str(random.randint(100000, 999999))
            assignment_date = random.choice(random_dates)
            academic_degree_id = str(uuid4())
            cursor.execute(f"INSERT INTO HR_ERP_ACADEMIC_DEGREES (PROFILE_ID, DEGREE_ID, SCIENCE_ID, SPECIALTY_ID, DOCUMENT_NUMBER, ASSIGNMENT_DATE, ID, CREATED_AT, UPDATED_AT) VALUES ('{educational_profile_id}', '{degree_id}', '{science_id}', '{specialty_id}', '{document_number}', TO_DATE('{assignment_date}', 'YYYY-MM-DD'), '{academic_degree_id}', SYSDATE, SYSDATE)")
            cursor.close()
    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            cursor = conn.cursor()
            academic_title_id = str(uuid4())
            degree_id = random.choice(['99962544-80a3-4fa4-a5b3-e526c780ae3f', 'a7b81b39-7030-4d68-abd4-d84cb049caf7'])
            specialty_id = random.choice(specialties)[2]
            document_number = str(random.randint(100000, 999999))
            assignment_date = random.choice(random_dates)
            cursor.execute(f"INSERT INTO HR_ERP_ACADEMIC_TITLES (PROFILE_ID, DEGREE_ID, SPECIALTY_ID, DOCUMENT_NUMBER, ASSIGNMENT_DATE, ID, CREATED_AT, UPDATED_AT) VALUES ('{educational_profile_id}', '{degree_id}', '{specialty_id}', '{document_number}', TO_DATE('{assignment_date}', 'YYYY-MM-DD'), '{academic_title_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            cursor = conn.cursor()
            education_id = str(uuid4())
            is_military_school = random.choice([0, 2])
            specialty_id = random.choice(specialties)[2]
            print(random.choice(specialties))
            type_of_top = random.choice(["Бакалавриат", "Магистратура"])
            document_number = str(random.randint(100000, 999999))
            date_of_issue = random.choice(random_dates)
            start_date = random.choice(random_dates)
            end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            institution_id = random.choice(institutions)[2]
            print(random.choice(institutions))
            degree_id = ['051afd14-2825-46ad-ba30-38f569946600',
        '4bbcebe4-ba0a-4e86-aaee-9233fed299ce',
        '4a64f581-b36b-42a6-b464-737a1306ea1a',
        'a822c476-2faa-4a4a-94bb-ebf07569a41a']
            degree_id = random.choice(degree_id)
            document_link = 'null'
            cursor.execute(f"INSERT INTO HR_ERP_EDUCATIONS (PROFILE_ID, IS_MILITARY_SCHOOL, SPECIALTY_ID, TYPE_OF_TOP, DOCUMENT_NUMBER, DATE_OF_ISSUE, START_DATE, END_DATE, INSTITUTION_ID, DEGREE_ID, DOCUMENT_LINK, ID, CREATED_AT, UPDATED_AT) VALUES ('{educational_profile_id}', '{is_military_school}', '{specialty_id}', '{type_of_top}', '{document_number}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), TO_DATE('{start_date}', 'YYYY-MM-DD'), TO_DATE('{end_date}', 'YYYY-MM-DD'), '{institution_id}', '{degree_id}', null, '{education_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):        
            cursor = conn.cursor()
            language_proficiency_id = str(uuid4())
            language_id = random.choice(languages)[2]
            level = random.randint(1, 5)
            document_number = str(random.randint(100000, 999999))
            assignment_date = random.choice(random_dates)
            user_id = new_id
            cursor.execute(f"INSERT INTO HR_ERP_LANGUAGE_PROFICIENCIES (LANGUAGE_ID, LANGUAGE_LEVEL, DOCUMENT_NUMBER, ASSIGNMENT_DATE, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{language_id}', '{level}', '{document_number}', TO_DATE('{assignment_date}', 'YYYY-MM-DD'), '{educational_profile_id}', '{language_proficiency_id}', SYSDATE, SYSDATE)")
            cursor.close()
    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):            
            cursor = conn.cursor()
            driving_license_id = str(uuid4())
            document_number = str(random.randint(100000, 999999))
            category = random.choice(["A", "B", "C", "D", "E"])
            date_of_issue = random.choice(random_dates)
            date_to = (datetime.strptime(date_of_issue, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            cursor.execute(f"INSERT INTO HR_ERP_DRIVING_LICENSES (DOCUMENT_NUMBER, CATEGORY, DATE_OF_ISSUE, DATE_TO, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{document_number}', '{category}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), TO_DATE('{date_to}', 'YYYY-MM-DD'), '{personal_profile_id}', '{driving_license_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            cursor = conn.cursor()
            identification_card_id = str(uuid4())
            document_number = str(random.randint(100000, 999999))
            date_of_issue = random.choice(random_dates)
            date_to = (datetime.strptime(date_of_issue, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            issued_by = random.choice(["МВД", "МИД"])
            cursor.execute(f"INSERT INTO HR_ERP_IDENTIFICATION_CARDS (DOCUMENT_NUMBER, DATE_OF_ISSUE, DATE_TO, ISSUED_BY, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{document_number}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), TO_DATE('{date_to}', 'YYYY-MM-DD'), '{issued_by}', '{personal_profile_id}', '{identification_card_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):        
            cursor = conn.cursor()
            sport_achievement_id = str(uuid4())
            sport_type_id = random.choice(sport_types)[2] 
            assignment_date = random.choice(random_dates)
            name = random.choice(["Золото", "Серебро", "Бронза"])
            name_kz = random.choice(["Алтын", "Алтын", "Алтын"])
            cursor.execute(f"INSERT INTO HR_ERP_SPORT_ACHIEVEMENTS (SPORT_TYPE_ID, ASSIGNMENT_DATE, NAME, NAMEKZ, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{sport_type_id}', TO_DATE('{assignment_date}', 'YYYY-MM-DD'), '{name}', '{name_kz}', '{personal_profile_id}', '{sport_achievement_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):        
            cursor = conn.cursor()
            sport_degree_id = str(uuid4())
            sport_degree_type_id = random.choice(sport_degree_types)[2]
            sport_type_id = random.choice(sport_types)[2]
    
            print(random.choice(sport_degree_types))
            assignment_date = random.choice(random_dates)
            cursor.execute(f"INSERT INTO HR_ERP_SPORT_DEGREES (PROFILE_ID, SPORT_DEGREE_TYPE_ID, SPORT_TYPE_ID, ASSIGNMENT_DATE, ID, CREATED_AT, UPDATED_AT) VALUES ('{personal_profile_id}', '{sport_degree_type_id}', '{sport_type_id}', TO_DATE('{assignment_date}', 'YYYY-MM-DD'), '{sport_degree_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):            
            cursor = conn.cursor()
            tax_declaration_id = str(uuid4())
            year = str(random.choice([2000, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2019, 2018, 2017, 2016, 2015]))
            is_paid = random.choice([0, 1])
            cursor.execute(f"INSERT INTO HR_ERP_TAX_DECLARATIONS (YEAR, IS_PAID, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{year}', '{is_paid}', '{personal_profile_id}', '{tax_declaration_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):            
            cursor = conn.cursor()
            user_financial_id = str(uuid4())
            iban = "".join([str(random.randint(0, 9)) for _ in range(20)])
            housing_payments_iban = "".join([str(random.randint(0, 9)) for _ in range(20)])
            cursor.execute(f"INSERT INTO HR_ERP_USER_FINANCIAL_INFOS (IBAN, HOUSING_PAYMENTS_IBAN, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{iban}', '{housing_payments_iban}', '{personal_profile_id}', '{user_financial_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            cursor = conn.cursor()
            abroad_travel_id = str(uuid4())
            country = random.choice(countries_db)[2]
            print(random.choice(countries_db))
            vehicle_types_id = random.choice(['00890df5-dd8d-4980-98b9-debd5fccfcfd', '2542f546-7398-4c73-954a-2b3922846beg', 'b74cbded-f4de-4c92-9935-6f7846b4dc85'])
            date_from = random.choice(random_dates)
            date_to = (datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            reason = random.choice(["Отдых", "Работа"])
            reason_kz = random.choice(["Демалу", "Жұмыс"])
            destination_country_id = random.choice(countries_db)[2]
            cursor.execute(f"INSERT INTO HR_ERP_ABROAD_TRAVELS (VEHICLE_TYPE_ID, DESTINATION_COUNTRY_ID, DATE_FROM, DATE_TO, REASON, REASONKZ, DOCUMENT_LINK, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{vehicle_types_id}', '{destination_country_id}', TO_DATE('{date_from}', 'YYYY-MM-DD'), TO_DATE('{date_to}', 'YYYY-MM-DD'), '{reason}', '{reason_kz}', null, '{additional_profile_id}', '{abroad_travel_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):        
            cursor = conn.cursor()
            polygraph_id = str(uuid4())
            number = str(random.randint(100000, 999999))
            issued_by = random.choice(["МВД", "МИД"])
            date_of_issue = random.choice(random_dates)
            cursor.execute(f"INSERT INTO HR_ERP_POLYGRAPH_CHECKS (POLYGRAPH_NUMBER, ISSUED_BY, DATE_OF_ISSUE, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{number}', '{issued_by}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), '{additional_profile_id}', '{polygraph_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            cursor = conn.cursor()
            psychophysiological_id = str(uuid4())
            issued_by = random.choice(["МВД", "МИД"])
            date_of_issue = random.choice(random_dates)
            document_number = str(random.randint(100000, 999999))
            cursor.execute(f"INSERT INTO HR_ERP_PSYCHOLOGICAL_CHECKS (ISSUED_BY, DATE_OF_ISSUE, DOCUMENT_NUMBER, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{issued_by}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), '{document_number}', '{additional_profile_id}', '{psychophysiological_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):            
            cursor = conn.cursor()
            service_housing_id = str(uuid4())
            type_properties = random.choice(['4bc287dc-04af-428f-b487-47509faa7c03',
        'c6964ff1-29ca-41e6-9a1d-592e466d67b5',
        'c583af55-8cd9-4510-8989-e4217f794694',
        'e63eaf6e-b11b-446c-88dc-06dd518c40dc'])
            address = random.choice(addresses)
            issue_date = random.choice(random_dates)
            cursor.execute(f"INSERT INTO HR_ERP_SERVICE_HOUSINGS (TYPE_ID, ADDRESS, ISSUE_DATE, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{type_properties}', '{address}', TO_DATE('{issue_date}', 'YYYY-MM-DD'), '{additional_profile_id}', '{service_housing_id}', SYSDATE, SYSDATE)")
            cursor.close()
    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):            
            cursor = conn.cursor()
            special_check_id = str(uuid4())
            number = str(random.randint(100000, 999999))
            issued_by = random.choice(["МВД", "МИД"])
            date_of_issue = random.choice(random_dates)
            cursor.execute(f"INSERT INTO HR_ERP_SPECIAL_CHECKS (SPECIAL_NUMBER, ISSUED_BY, DATE_OF_ISSUE, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{number}', '{issued_by}', TO_DATE('{date_of_issue}', 'YYYY-MM-DD'), '{additional_profile_id}', '{special_check_id}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):        
            cursor = conn.cursor() 
            vehicle_id = str(uuid4())
            number = str(random.randint(100000, 999999))
            vin_code = "".join([str(random.randint(0, 9)) for _ in range(17)])
            date_from = random.choice(random_dates)
            name = random.choice(["BMW", "Mercedes", "Toyota", "Lada"])
            cursor.execute(f"INSERT INTO HR_ERP_USER_VEHICLES (VEHICLE_NUMBER, VIN_CODE, PROFILE_ID, ID, DATE_FROM, NAME, NAMEKZ, CREATED_AT, UPDATED_AT) VALUES ('{number}', '{vin_code}', '{additional_profile_id}', '{vehicle_id}', TO_DATE('{date_from}', 'YYYY-MM-DD'), '{name}', '{name}', SYSDATE, SYSDATE)")
            cursor.close()

    test = random.choice([0, 1])
    if test == 1:
        for i in range(random.randint(0, 5)):
            
            cursor = conn.cursor()
            violation_id = str(uuid4())
            name = random.choice(["Пьяный за рулем", "Превышение скорости"])
            name_kz = random.choice(["Саулыққа қарсы", "Саулыққа қарсы"])
            date = random.choice(random_dates)
            issued_by = random.choice(["МВД", "МИД"])
            issued_by_kz = random.choice(["МВД", "МИД"])
            article_number = str(random.randint(100000, 999999))
            article_number_kz = str(random.randint(100000, 999999))
            consequence = random.choice(["Штраф", "Лишение прав"])
            consequence_kz = random.choice(["Штраф", "Лишение прав"])
            cursor.execute(f"INSERT INTO HR_ERP_VIOLATIONS (NAME, NAMEKZ, ISSUED_BY, ISSUED_BYKZ, ARTICLE_NUMBER, ARTICLE_NUMBERKZ, CONSEQUENCE, CONSEQUENCEKZ, PROFILE_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{name}', '{name_kz}', '{issued_by}', '{issued_by_kz}', '{article_number}', '{article_number_kz}', '{consequence}', '{consequence_kz}', '{additional_profile_id}', '{violation_id}', SYSDATE, SYSDATE)")
            cursor.close()
    test = random.choice([0, 1])
    if test == 1:    
        cursor = conn.cursor()
        service_id = str(uuid4())
        number = str(random.randint(100000, 999999))
        date_to = random.choice(random_dates)
        token_status = random.choice(["Получен", "Не получен", "Утерян"])
        id_status = random.choice(["Получен", "Не получен", "Утерян"])
        user_id = new_id

        cursor.execute(f"INSERT INTO HR_ERP_SERVICE_IDS (SERVICE_NUMBER, DATE_TO, TOKEN_STATUS, ID_STATUS, USER_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{number}', TO_DATE('{date_to}', 'YYYY-MM-DD'), '{token_status}', '{id_status}', '{user_id}', '{service_id}', SYSDATE, SYSDATE)")
        cursor.close()
    
    cursor = conn.cursor()
    personal_reserves_id = str(uuid4())
    reserve = random.choice(["Зачислен", "Резерв"])
    reserve_date = random.choice(random_dates)
    user_id = new_id

    cursor.execute(f"INSERT INTO HR_ERP_PERSONNAL_RESERVES (RESERVE, RESERVE_DATE, USER_ID, ID, CREATED_AT, UPDATED_AT) VALUES ('{reserve}', TO_DATE('{reserve_date}', 'YYYY-MM-DD'), '{user_id}', '{personal_reserves_id}', SYSDATE, SYSDATE)")

    cursor.close()
     


    

conn.commit()

conn.close()
    
    


    

    


    







    

