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
dsn_tns = cx_Oracle.makedsn('192.168.0.61', '1521', service_name='MORAL')
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
    call_sign = str(random.choice(["Альфа", "Бетта", "Гамма"]) + str(random.randint(0, 999999999)))
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
    print("done")
conn.commit()
conn.close()
    
    


    

    


    







    

