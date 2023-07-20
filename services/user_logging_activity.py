from sqlalchemy.orm import Session

from models import UserLoggingActivity


class UserLoggingActivityService:
    
    def create(self, db: Session, user_id):
        obj = UserLoggingActivity(user_id=user_id)
        
        db.add(obj)
        db.flush()
        
        return obj

    def get_activities_of_user(self, db: Session, user_id):
        return db.query(UserLoggingActivity).filter(
            UserLoggingActivity.user_id == user_id
        ).all()

user_logging_activity_service = UserLoggingActivityService()