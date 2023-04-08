from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import Profile
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
        return profile

    def generate_profile_doc(self, db: Session, user_id: str):
        profile = self.get_by_user_id(db, user_id)

        # data = {
        #     "last_name": profile.user.last_name,
        #     "first_name": profile.user.first_name,
        #     "father_name": profile.user.father_name,
        #     "iin": "",
        #     "id_number": profile.user.id_number,
        #     "rank": profile.user.rank,
        #     "by_order": "",
        #     "date_birth": profile.user.
        # }

        print(profile.user.last_name)

        return


profile_service = ProfileService(Profile)
