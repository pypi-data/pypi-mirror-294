from user_service.users.model.api import session
from user_service.users.model import models

class UserRepository(object):
    def __init__(self):
        self.session = session

    def users_list(self):
        return self.session.query(
            models.UserTable).all()

    def users_get(self, user_name):
        return self.session.query(
            models.UserTable).filter_by(username=user_name).first()

    def users_delete(self, user_id):
        (self.session.query(
            models.UserTable).
         filter_by(id=user_id).delete())
        self.session.commit()


    def users_create(self, values):
        user = models.UserTable().set_user(values)
        self.session.add(user)
        self.session.commit()
        return user

    def users_update(self, user_id, user):
        (self.session.query(
            models.User).
         filter_by(id=user_id).update(user))
        self.session.commit()
        return user


db_api = UserRepository()