from dto.user import User


class Doctor:
    def __init__(self, result):
        self.doctorId = result['doctor_id'] if 'doctor_id' in result else ''
        self.fullName = result['full_name'] if 'full_name' in result else ''
        self.speciality = result['specialty'] if 'specialty' in result else ''
        self.email = result['email'] if 'email' in result else ''
        self.phone = result['phone'] if 'phone' in result else ''
        self.user = User(None, result['username'] if 'username' in result else '')
