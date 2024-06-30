from dto.doctor import Doctor
from service.db import MySql


class DoctorService:
    def __init__(self):
        self.db = MySql()

    def get_doctors(self):
        query = """
            select d.doctor_id, d.full_name, d.phone, d.email, d.specialty, u.username
            from doctor d
                     inner join users u on d.user_id = u.user_id
            where u.status = 'active';
        """
        result = self.db.select(query)
        return [Doctor(row) for row in result]

    def add_doctor(self, doctor):
        index0 = '{0}'
        query1 = f"INSERT INTO users(username, password, role, status) VALUES ('{doctor[0]}', '{doctor[1]}', 'doctor', 'active')"
        query2 = f"insert into doctor(user_id, full_name, specialty, email, phone) VALUES ('{index0}', '{doctor[2]}', '{doctor[3]}', '{doctor[4]}', '{doctor[5]}')"
        return self.db.execute2(query1, query2)

    def update_doctor(self, data1):
        try:
            query1 = f"""
                UPDATE doctor
                SET full_name = '{data1[0]}',
                    specialty = '{data1[1]}',
                    phone = '{data1[2]}',
                    email = '{data1[3]}'
                WHERE doctor_id = {data1[4]}
            """
            self.db.execute(query1)
            return True
        except Exception as e:
            print(e)
            return False

    def update_password(self, username, password):
        query = f"UPDATE users SET password = '{password}' WHERE username = '{username}'"
        return self.db.execute(query)

    def delete_doctor(self, doctorId):
        query = f"""
                    update users u
                    inner join doctor p on u.user_id = p.user_id
                    set u.status = 'inactive'
                    where p.doctor_id = {doctorId};
                """
        try:
            self.db.execute(query)
            return True
        except Exception as e:
            print(e)
            return False
