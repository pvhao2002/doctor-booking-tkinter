from dto.victim import Victim
from service.db import MySql


class VictimService:
    def __init__(self):
        self.db = MySql()

    def get_victims(self):
        query = """
                select p.victim_id, p.full_name, p.gender, p.birthday, p.address, p.phone, p.age, u.username
                from victim p
                         inner join users u on p.user_id = u.user_id
                where u.status = 'active';
        """
        result = self.db.select(query)
        return [Victim(row) for row in result]

    def get_info(self, uid):
        query = f"""
            select p.*,
                   u.username,
                   u.password
            from victim p
                     inner join users u on p.user_id = u.user_id
            where u.role = 'victim'
              and u.status = 'active'
              and u.user_id = '{uid}';
                """
        result = self.db.select(query)
        return Victim(result[0]).set_password(result[0]['password'])

    def add_victims(self, victim):
        index0 = '{0}'
        query1 = f"INSERT INTO users(username, password, role, status) VALUES ('{victim[0]}', '{victim[1]}', 'victim', 'active')"
        query2 = f"INSERT INTO victim(full_name, gender, birthday, address, phone, age, user_id) VALUES ('{victim[2]}', '{victim[3]}', '{victim[4]}', '{victim[5]}', '{victim[6]}', '{victim[7]}', '{index0}')"
        return self.db.execute2(query1, query2)

    def update_password(self, username, password):
        query = f"UPDATE users SET password = '{password}' WHERE username = '{username}'"
        return self.db.execute(query)

    def update_victims(self, victim):
        query = f"""
                UPDATE victim
                SET full_name = '{victim[0]}',
                    gender = '{victim[1]}',
                    birthday = '{victim[2]}',
                    address = '{victim[3]}',
                    phone = '{victim[4]}',
                    age = '{victim[5]}'
                WHERE victim_id = {victim[6]}
        """
        try:
            self.db.execute(query)
            return True
        except:
            return False

    def delete_victims(self, victim_id):
        query = f"""
            update users u
            inner join victim p on u.user_id = p.user_id
            set u.status = 'inactive'
            where p.victim_id = {victim_id};
        """
        try:
            self.db.execute(query)
            return True
        except:
            return False
