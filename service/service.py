from dto.service import Service
from service.db import MySql


class ServiceService:
    def __init__(self):
        self.db = MySql()

    def get_services(self):
        query = """
                    select *
                    from services
                    where status = 'active';
        """
        result = self.db.select(query)
        return [Service(row) for row in result]

    def get_one_service(self, service_id):
        query = f"""
                    select *
                    from services
                    where service_id = '{service_id}' and status = 'active';
        """
        result = self.db.select(query)
        return Service(result[0]) if result and len(result) > 0 else None

    def add_services(self, s):
        query1 = f"insert into services(service_name, description, price, status) VALUES ('{s[0]}', '{s[1]}', '{s[2]}', 'active')"
        return self.db.execute(query1)

    def update_services(self, data1):
        try:
            query1 = f"""
                        update services
                        set service_name = '{data1[0]}',
                            description = '{data1[1]}',
                            price = '{data1[2]}'
                        where service_id = '{data1[3]}';
            """
            self.db.execute(query1)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_services(self, service_id):
        query = f"""
                    update services
                    set status = 'inactive'
                    where service_id = '{service_id}';
                """
        try:
            self.db.execute(query)
            return True
        except Exception as e:
            print(e)
            return False
