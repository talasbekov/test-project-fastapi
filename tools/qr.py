import cx_Oracle
from names import generate_names, generate_phone_number, addresses, random_dates, ad, add, adf
from uuid import uuid4
import random
def convert_lob_to_str(obj):
    if isinstance(obj, cx_Oracle.LOB):
        return obj.read()
    elif isinstance(obj, dict):
        return {k: convert_lob_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_lob_to_str(elem) for elem in obj]
    else:
        return obj
SQLALCHEMY_DATABASE_URL = f"oracle+cx_oracle://hr:hr2025@192.168.1.86:1521/hrfree"
# Create a connection to the Oracle database
dsn_tns = cx_Oracle.makedsn('192.168.1.86', '1521', service_name='hrfree')
conn = cx_Oracle.connect(user='hr', password='hr2025', dsn=dsn_tns)

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
    curator_of_id = None
    staff_division = random.choice(divisions)[6]
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO HR_ERP_STAFF_UNITS (POSITION_ID, STAFF_DIVISION_ID, USER_REPLACING_ID, ID, CURATOR_OF_ID, IS_ACTIVE, CREATED_AT, UPDATED_AT, REQUIREMENTS, TRIAL257, ACTUAL_POSITION_ID) VALUES ('{actual_position}', '{staff_division}', null, '{staff_unit_id}', null, '{is_active}', SYSDATE, SYSDATE, null, null, '{actual_position}')") 
    conn.commit()
    cursor.close()


    # profile
     


    # badges

    # example of cabinet: 1.2.217K random
 

    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO HR_ERP_USERS (EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, FATHER_NAME, CALL_SIGN, ID_NUMBER, PHONE_NUMBER, ADDRESS, RANK_ID, STAFF_UNIT_ID, ACTUAL_STAFF_UNIT_ID, IS_ACTIVE, SUPERVISED_BY, CABINET, SERVICE_PHONE_NUMBER, IS_MILITARY, PERSONAL_ID, IIN, DATE_BIRTH, ID, LAST_SIGNED_AT, CREATED_AT, UPDATED_AT, TRIAL346, DESCRIPTION, ICON) VALUES ('{email}', '{password}', '{first_name}', '{last_name}', '{father_name}', '{call_sign}', '{id_number}', '{phone_number}', '{address}', '{rank_id}', '{staff_unit_id}', '{staff_unit_id}', '{is_active}', null, '{cabinet}', '{service_phone_number}', '{is_military}', '{personal_id}', '{iin}', TO_DATE('{date_birth}', 'YYYY-MM-DD'), '{new_id}', null, SYSDATE, SYSDATE, null, null, '{icon}')") 
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    badge_id = str(uuid4())
    badges_len = len(badge_types)
    badge_type = random.choice(badge_types)
    
    print(badge_type)
    for i in random.sample(range(badges_len), random.randint(0, badges_len)):
        badge_new_id = str(uuid4())
        cursor.execute(f"INSERT INTO HR_ERP_BADGES (TYPE_ID, USER_ID, ID, CREATED_AT, UPDATED_AT, TRIAL774) VALUES ('{badge_type[1]}', '{new_id}', '{badge_new_id}', SYSDATE, SYSDATE, null)") 
    conn.commit()
    cursor.close()


    cursor = conn.cursor()
    profile_id = str(uuid4())
    cursor.execute(f"INSERT INTO HR_ERP_PROFILES (USER_ID, ID, CREATED_AT, UPDATED_AT, TRIAL117) VALUES ('{new_id}', '{profile_id}', SYSDATE, SYSDATE, null)") 
    conn.commit()
    cursor.close()



    







    

