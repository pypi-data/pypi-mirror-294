from user_service.users.repository.user import User

class RegisterService(object):
    def __init__(self):
        pass

    def register_user(self, user):
        if User().user_create(user):
            return "Registered successfully."
        return "User already exists."