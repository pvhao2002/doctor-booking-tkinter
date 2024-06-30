from itertools import groupby

from dto.appointment import Appointment
from dto.invoice_detail import InvoiceDetail
from service.db import MySql


class BookingService:
    def __init__(self):
        self.db = MySql()

    def book_appointment(self, data):
        try:
            query = f"INSERT INTO appointment(victim_id, doctor_id, appointment_date, status) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', 'pending')"
            self.db.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def get_appointment(self, victim_id):
        query = f"""
            select ap.appointment_id,
                   ap.doctor_id,
                   d.full_name,
                   ap.appointment_date,
                   ap.status
            from appointment ap
                     inner join doctor d on ap.doctor_id = d.doctor_id
            where ap.victim_id = '{victim_id}'
            order by ap.appointment_date desc;
        """
        result = self.db.select(query)
        return [Appointment(appointment) for appointment in result]

    def get_doctor_appointment(self, doctor_id):
        query = f"""
            select ap.appointment_id,
                   ap.victim_id,
                   p.full_name,
                   p.phone,
                   p.age,
                   p.address,
                   ap.appointment_date,
                    ap.status
            from appointment ap
                     inner join victim p on ap.victim_id = p.victim_id
                     inner join doctor d on ap.doctor_id = d.doctor_id
                     inner join users u on u.user_id = d.user_id
            where u.user_id = '{doctor_id}'
              and (ap.status = 'pending' or ap.status = 'accepted') 
            order by ap.appointment_date desc;
        """
        result = self.db.select(query)
        return [Appointment(appointment) for appointment in result]

    def update_status_appointment(self, appointment_id, status):
        try:
            query = f"UPDATE appointment SET status = '{status}' WHERE appointment_id = {appointment_id} and status = 'pending'"
            self.db.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def create_bill(self, data, list_service):
        query1 = f"""
        insert into invoice(appointment_id, total_amount, create_date, payment_status) values ('{data[0]}', '{data[1]}', now(), '{data[2]}')
        """
        try:
            last_id = self.db.execute_without_commit(query1)
            query2 = f"""
                        insert into invoice_detail(invoice_id, service_id) VALUES 
                    """
            for i, service in enumerate(list_service):
                query2 += f"('{last_id}', '{service['id']}')"
                if i < len(list_service) - 1:
                    query2 += ','
            self.db.execute_without_commit(query2)

            query3 = f"UPDATE appointment SET status = 'completed' WHERE appointment_id = {data[0]}"
            self.db.execute(query3)
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def get_invoice(self, appointment_id):
        query = f"""
        select i.invoice_id,
               i.total_amount,
               i.create_date,
               i.payment_status,
               s.service_id,
               s.service_name,
               s.price
        from invoice i
        inner join invoice_detail id on i.invoice_id = id.invoice_id
        inner join services s on id.service_id = s.service_id
        where appointment_id = '{appointment_id}';
        """
        return self.db.select(query)

    def get_all_invoice(self):
        query = f"""
        select i.invoice_id,
               i.total_amount,
               i.create_date,
               i.payment_status,
               s.service_id,
               s.service_name,
               s.price
        from invoice i
        inner join invoice_detail id on i.invoice_id = id.invoice_id
        inner join services s on id.service_id = s.service_id
        """
        rs = self.db.select(query)
        list_invoice = []
        for key, group in groupby(rs, key=lambda x: x['invoice_id']):
            invoice = list(group)
            invoice_detail = InvoiceDetail(invoice)
            list_invoice.append(invoice_detail)
        return list_invoice
