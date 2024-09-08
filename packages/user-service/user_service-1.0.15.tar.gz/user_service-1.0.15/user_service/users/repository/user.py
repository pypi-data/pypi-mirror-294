from user_service.users.repository.user_repository import db_api
from user_service.users.model.models import UserTable

class User(object):
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self.db = db_api

    def user_create(self, values):
        self.db.users_create(values)
        return True

    def is_exists(self):
        if  (self.username in
                [self.db.users_get(self.username).username]):
            return True
        return False


