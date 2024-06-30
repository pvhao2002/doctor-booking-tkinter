from dto.doctor import Doctor
from dto.victim import Victim


class Appointment:
    def __init__(self, result):
        self.appointment_id = result['appointment_id'] if 'appointment_id' in result else ''
        self.victim = Victim(result)
        self.doctor = Doctor(result)
        self.appointment_date = result['appointment_date'] if 'appointment_date' in result else ''
        self.status = result['status'] if 'status' in result else ''
