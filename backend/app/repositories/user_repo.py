from app.models.user import User


class UserRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> User:
        user = User(**payload)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self):
        return self.db.query(User).all()
