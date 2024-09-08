from user_service.users.repository import user_repository
from user_service.users.repository.user import User


class LoginService(object):
    def __init__(self):
        self.dbapi = user_repository.db_api

    def validate_login(self, user: str, email:str, password:str) -> bool:
        """
        This is Business login service for Login.
        :param user:
        :param email:
        :param password:
        :return:
        """
        try:
            user_obj = User(username=user,
                            email=email, password=password)
            if user_obj.is_exists():
                return "Login successful."
            return "User does not exist. please register First."
        except Exception as ex:
            return False
