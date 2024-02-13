import json
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import Profile, Liberation
from schemas import ProfileCreate, ProfileUpdate
from services import ServiceBase


class ProfileService(ServiceBase[Profile, ProfileCreate, ProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        profile = super().get(db, id)
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with id: {id} is not found!")
        return profile

    def get_by_user_id(self, db: Session, id: str) -> Profile:
        profile = db.query(self.model).filter(self.model.user_id == id).first()
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with user_id: {id} is not found!")
        if profile.personal_profile is not None:
            if profile.personal_profile.driving_license is not None:
                profile.personal_profile.driving_license.category = (
                    eval(profile.personal_profile.driving_license.category)
                    if isinstance(profile.personal_profile.driving_license.category, str)
                    else profile.personal_profile.driving_license.category
                )
        return profile

    # def generate_profile_doc(self, db: Session, user_id: str):
    #     profile = self.get_by_user_id(db, user_id)
    #     education = max(profile.educational_profile.education,
    #                     key=lambda obj: obj.end_date)
    #     institutions = (
    #     education.institution.name
    #     for education in profile.educational_profile.education
    #     if not education.is_military_school)
    #     military_institutions = (
    #     education.institution.name for education
    #     in profile.educational_profile.education if education.is_military_school)
    #     academic_degrees = (AcademicDegreeRead.from_orm(academic_degree).dict()
    #     for academic_degree in profile.educational_profile.academic_degree)
    #     abroad_travels = (AbroadTravelRead.from_orm(abroad_travel).dict()
    #     for abroad_travel in profile.additional_profile.abroad_travels)
    #    language_proficiencies = (
    #    LanguageProficiencyRead.from_orm(language_proficiency).dict()
    #    for language_proficiency in profile.educational_profile.language_proficiency)
    #     sport_degrees = (SportDegreeRead.from_orm(sport_degree).dict()
    # for sport_degree in profile.personal_profile.sport_degrees)

    #     docx_context_data = {
    #         "last_name": profile.user.last_name,
    #         "first_name": profile.user.first_name,
    #         "father_name": profile.user.father_name,
    #         "iin": "",
    #         "id_number": profile.user.id_number,
    #         "rank": profile.user.rank.name,
    #         "by_order": "",  # TODO: СЛУЖБА И РЕКВИЗИТЫ
    #         "date_birth": "profile.user.birth_date",
    #         "place_birth": profile.personal_profile.biographic_info.place_birth,
    #         "nationality": profile.personal_profile.biographic_info.nationality,
    #         "institution_degree_type_name": education.degree.name,
    #         "institutions": list(institutions),
    #         "military_institutions": list(military_institutions),
    #         "academic_degrees": [],
    #         "abroad_travels": list(abroad_travels),
    #         "language_proficiencies": list(language_proficiencies),
    #         "sport_degrees": list(sport_degrees),
    #         "categories": list(profile.personal_profile.driving_license.category),
    #         "blood_group":
    #           profile.medical_profile.general_user_info[0].blood_group.value
    #     }

    #     template_path = configs.TEMPLATE_FILE_PATH+"Послужной список.docx"
    #     generated_file_name = "Послужной список резалт.docx"
    #     generated_file_path = configs.GENERATED_FILE_PATH+"/"+generated_file_name

    #     template_file = DocxTemplate(template_path)
    #     template_file.render(docx_context_data)
    #     template_file.save(generated_file_path)

    #     return {
    #         "file_location": generated_file_path,
    #         "file_name": generated_file_name
    #     }


profile_service = ProfileService(Profile)
