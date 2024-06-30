from service.db import MySql
from dto.user import User


class UserService:
    def __init__(self):
        self.db = MySql()

    def login(self, username, password):
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}' AND status = 'active'"
        result = self.db.select(query)
        if len(result) == 0:
            return None
        return User(result[0])

    def register(self, username, password, full_name):
        try:
            query = f"INSERT INTO users(username, password, role, status) VALUES ('{username}', '{password}', 'victim', 'active')"
            last_user_id = self.db.execute(query)

            new_query = f"INSERT INTO victim(user_id, full_name) VALUES ({last_user_id}, '{full_name}')"
            self.db.execute(new_query)
            return True
        except:
            return False
