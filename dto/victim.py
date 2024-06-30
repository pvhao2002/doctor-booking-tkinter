from dto.user import User


def get_gender(gender):
    if gender == 'MALE':
        return 'Nam'
    elif gender == 'FEMALE':
        return 'Nữ'
    else:
        return 'Khác'


class Victim:
    def __init__(self, result):
        self.victimId = result['victim_id'] if 'victim_id' in result else ''
        self.fullName = result['full_name'] if 'full_name' in result else ''
        self.gender = get_gender(result['gender'] if 'gender' in result else 'OTHER')
        self.birthDate = result['birthday'] if 'birthday' in result else ''
        self.address = result['address'] if 'address' in result else ''
        self.phone = result['phone'] if 'phone' in result else ''
        self.age = result['age'] if 'age' in result else ''
        self.user = User(None, result['username'] if 'username' in result else '')

    def set_password(self, password):
        self.user = self.user.set_password(password)
        return self

    def __str__(self):
        return f"Victim {self.victimId}: {self.fullName}, {get_gender(self.gender)}, {self.birthDate}, {self.address}, {self.phone}, {self.age}, {self.user.username}"
