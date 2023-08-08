import psycopg2

host = 'localhost'
database = 'sgo-erp'
user = 'postgres'
password = '123'
prefix = 'HR_ERP_'

connection = psycopg2.connect(
    host=host, database=database, user=user, password=password, port=5412
)

cursor = connection.cursor()

cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
table_names = cursor.fetchall()

for table_name in table_names:
    old_name = table_name[0]
    new_name = prefix + old_name
    cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name};")
    print(f"Table {old_name} renamed to {new_name}")

connection.commit()
cursor.close()

"""
alembic_version
staff_division_types
staff_divisions
ranks
positions
document_function_types
arch_doc_fun_types
service_function_types
arch_ser_func_type
candidate_stage_types
cand_stage_questions
users
candidate_essay_types
candidates
jurisdictions
type_army_equipments
type_ar_equip_models
type_cloth_equipmets
cloth_eq_types_models
type_cloth_eq_models
type_other_equipments
type_oth_eq_models
archive_staff_functions
attestations
badge_types
badges
candidate_stage_answers
candidate_categories
candidate_stage_infos
contract_types
contracts
coolness_types
coolnesses
equipments
events
hr_document_steps
name_changes
penalty_types
penalties
personnal_reserves
privelege_emergencies
profiles
recommender_users
service_ids
staff_unit_functions
s_u_cand_stage_infos
status_types
statuses
military_units
user_oaths
user_stats
additional_profiles
archive_staff_divisions
educational_profiles
family_profiles
hr_document_statuses
medical_profiles
personal_profiles
countries
abroad_travels
academic_degree_degrees
academic_degrees
sciences
specialties
academic_title_degrees
academic_titles
anthropometric_data
a_s_u_cand_stage_infos
family_statuses
biographic_infos
course_providers
courses
disp_registrations
driving_licenses
inst_degree_types
educations
institutions
families
family_relations
general_user_info
hospital_datas
hr_document_equipments
hr_document_infos
hr_document_users
identification_cards
languages
passports
polygraph_checks
properties
property_types
psychological_checks
service_housings
special_checks
sport_achievements
sport_types
sport_degrees
tax_declarations
user_financial_infos
liberations
user_liberations
user_vehicles
violations
family_violations
family_abroad_travels
academic_degree_degrees
a_s_u_func
u_liber_liberations
hr_vacancies
hr_v_hr_vacancy_req
hr_vac_req
hr_documents
notifications
hr_vacancy_candidates
archive_staff_units
staff_units
secondments
state_bodies
histories
staff_lists
staff_functions
language_proficiencies
questions
options
answers_options
activities
bsp_plans
places
exam_schedules
schedule_exam_months
schedule_months
schedule_year_months
schedule_year_s_d
schedule_year_users
exam_results
exam_schedule_inst
schedule_month_instr
answers
attendances
attended_users
hr_document_templates
user_logging_activities
days
surveys
schedule_years
months
activity_dates
activity_date_days
schedule_days
"""