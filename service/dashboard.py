from service.db import MySql


class DashboardService:
    def __init__(self):
        self.db = MySql()

    def dashboard(self):
        query1 = "select count(victim_id) as total_victim from victim"
        query2 = "select count(doctor_id) as total_doctors from doctor"
        query3 = "select count(service_id) as total_services from services"
        query4 = "select count(appointment_id) as total_appointments from appointment"
        query5 = """
        select count(victim_id) as total_victim
        from victim p
        where p.user_id in (select u.user_id from users u where u.status = 'active' and u.role = 'victim')
        """
        query6 = """
                select count(p.doctor_id) as total_doctor
                from doctor p
                where p.user_id in (select u.user_id from users u where u.status = 'active' and u.role = 'doctor')
                """
        result1 = self.db.select(query1)
        result2 = self.db.select(query2)
        result3 = self.db.select(query3)
        result4 = self.db.select(query4)
        result5 = self.db.select(query5)
        result6 = self.db.select(query6)
        return {
            'total_victim': result1[0]['total_victim'],
            'total_doctors': result2[0]['total_doctors'],
            'total_services': result3[0]['total_services'],
            'total_appointments': result4[0]['total_appointments'],
            'total_active_victim': result5[0]['total_victim'],
            'total_active_doctors': result6[0]['total_doctor']
        }
