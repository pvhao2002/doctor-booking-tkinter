class User:
    def __init__(self, result=None, username=None):
        if result:
            self.id = result['user_id'] if 'user_id' in result else ''
            self.username = result['username'] if 'username' in result else ''
            self.password = result['password'] if 'password' in result else ''
            self.role = result['role'] if 'role' in result else ''
            self.status = result['status'] if 'status' in result else ''
        else:
            self.id = None
            self.username = username
            self.password = None
            self.role = None
            self.status = None

    def set_password(self, password):
        self.password = password
        return self
