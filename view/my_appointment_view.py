import tkinter

import customtkinter as ctk

from service.booking import BookingService
from service.service import ServiceService
from utils.alert import show_warning, show_info


class ListAppointment(ctk.CTkScrollableFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.pack_propagate(False)
        self.service = BookingService()
        self.current_user = current_user
        self.parent = parent

        self.load_data()

    def load_data(self):
        my_appointment = self.service.get_doctor_appointment(self.current_user.id)

        headers = ["Mã đặt", "Mã bệnh nhân", "Tên bệnh nhân", "SDT", "Tuổi", "Địa chỉ", "Ngày", "#"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=70, height=25)
            header_label.grid(row=0, column=j, padx=5, pady=5)

        for i, b in enumerate(my_appointment, start=1):
            data = [b.appointment_id, b.victim.victimId, b.victim.fullName, b.victim.phone, b.victim.age,
                    b.victim.address, b.appointment_date]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=70, height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)

            if b.status == 'pending':
                accept_button = ctk.CTkButton(self, text="Chấp nhận", width=70, height=25,
                                              bg_color='green',
                                              fg_color='transparent', hover_color='dark green',
                                              command=lambda doc=b: self.accept_booking(doc))
                accept_button.grid(row=i, column=len(data), padx=5, pady=5)

            if b.status == 'accepted':
                create_bill_button = ctk.CTkButton(self, text="Lập hóa đơn", width=70, height=25,
                                                   bg_color='blue',
                                                   fg_color='transparent', hover_color='dark green',
                                                   command=lambda doc=b: self.create_bill(doc))
                create_bill_button.grid(row=i, column=len(data), padx=5, pady=5)

    def accept_booking(self, doc):
        result = self.service.update_status_appointment(doc.appointment_id, 'accepted')
        if result:
            self.load_data()
        else:
            msg = 'Chấp nhận thất bại'
            show_warning(msg)

    def create_bill(self, doc):
        self.parent.load_bill(doc)


class CreateBill(ctk.CTkScrollableFrame):
    def __init__(self, parent, appointment):
        super().__init__(parent)
        self.status_name_var = None
        self.list_status_name = None
        self.services_name_var = None
        self.list_services_to_id = None
        self.parent = parent
        self.s_service = ServiceService()
        self.appointment = appointment
        self.service = BookingService()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.list_services = []
        self.total_price = 0
        self.total_price_var = ctk.StringVar(value='0 VNĐ')

        self.list_status = {'Miễn phí': 'free', 'Đã thanh toán': 'paid'}

        # Frame cho dịch vụ
        self.frame_services = ctk.CTkFrame(self)
        self.frame_services.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        if appointment:
            self.load_appointment_info(appointment)
            self.load_services()

    def load_appointment_info(self, appointment):
        label_info = ctk.CTkLabel(self.frame, text='Lập hóa đơn',
                                  font=("Arial", 16))
        label_info.grid(row=0, column=0, pady=12, padx=10, columnspan=2)
        appointment = appointment
        # Mã lịch khám
        lb_appointment_id = ctk.CTkLabel(self.frame, text='Mã lịch khám')
        lb_appointment_id.grid(row=1, column=0, pady=2, padx=2, sticky="e")
        appointment_id = ctk.CTkLabel(self.frame,
                                      text=appointment.appointment_id)
        appointment_id.grid(row=1, column=1, pady=12, padx=10)

        # Mã bệnh nhân
        lb_victim_id = ctk.CTkLabel(self.frame, text='Mã bệnh nhân')
        lb_victim_id.grid(row=2, column=0, pady=2, padx=2, sticky="e")
        victim_id = ctk.CTkLabel(self.frame,
                                 text=appointment.victim.victimId)
        victim_id.grid(row=2, column=1, pady=12, padx=10)

        # Bệnh nhân
        lb_victim_name = ctk.CTkLabel(self.frame, text='Bệnh nhân')
        lb_victim_name.grid(row=5, column=0, pady=2, padx=2, sticky="e")
        victim_name_var = ctk.StringVar(value=appointment.victim.fullName)
        victim_name_selection = ctk.CTkLabel(self.frame,
                                             text=appointment.victim.fullName)
        victim_name_selection.grid(row=5, column=1, pady=12, padx=10)

        # Ngày khám bệnh
        lb_booking_date = ctk.CTkLabel(self.frame, text='Ngày khám')
        lb_booking_date.grid(row=6, column=0, pady=2, padx=2, sticky="e")
        booking_date = ctk.CTkLabel(self.frame,
                                    text=appointment.appointment_date)
        booking_date.grid(row=6, column=1, pady=12, padx=10)

        list_services = self.s_service.get_services()

        self.list_services_to_id = {service.service_name: service.service_id for service in list_services}
        list_services_name = list(self.list_services_to_id.keys())
        self.services_name_var = ctk.StringVar(value='Chọn dịch vụ')
        # Dịch vụ
        lb_service_name = ctk.CTkLabel(self.frame, text='Dịch vụ')
        lb_service_name.grid(row=7, column=0, pady=2, padx=2, sticky="e")
        service_name_selection = ctk.CTkComboBox(self.frame, values=list_services_name,
                                                 variable=self.services_name_var,
                                                 width=250)
        service_name_selection.grid(row=7, column=1, pady=12, padx=10)
        service_button = ctk.CTkButton(self.frame, text='Thêm dịch vụ', command=self.add_service)
        service_button.grid(row=7, column=2, pady=12, padx=10)

        # Thành tiền
        lb_total_price = ctk.CTkLabel(self.frame, text='Tổng tiền')
        lb_total_price.grid(row=8, column=0, pady=2, padx=2, sticky="e")
        total_price = ctk.CTkEntry(self.frame, textvariable=self.total_price_var, width=250, height=20,
                                   state=tkinter.DISABLED)
        total_price.grid(row=8, column=1, pady=12, padx=10)

        # status invoice
        self.list_status_name = list(self.list_status.keys())
        self.status_name_var = ctk.StringVar(value='Chọn trạng thái')
        lb_status = ctk.CTkLabel(self.frame, text='Trạng thái thanh toán')
        lb_status.grid(row=9, column=0, pady=2, padx=2, sticky="e")
        status_selection = ctk.CTkComboBox(self.frame, values=self.list_status_name,
                                           variable=self.status_name_var,
                                           width=250)
        status_selection.grid(row=9, column=1, pady=12, padx=10)

        # Lưu hóa đơn
        save_button = ctk.CTkButton(self.frame, text='Lưu hóa đơn', command=lambda: self.save_bill(appointment))
        save_button.grid(row=10, column=1, pady=12, padx=10)

    def add_service(self):
        selected_name = self.services_name_var.get()
        service_id = self.list_services_to_id.get(selected_name, None)
        if service_id is not None:
            service = self.s_service.get_one_service(service_id)
            for s in self.list_services:
                if s['id'] == service_id:
                    return
            self.list_services.append({'id': service_id, 'name': service.service_name, 'price': service.price})
            self.total_price += service.price
            self.total_price_var.set(str(self.total_price) + ' VNĐ')
            self.load_services()

    def load_services(self):
        # Destroy previous frame contents if any
        for widget in self.frame_services.winfo_children():
            widget.destroy()

        headers = ['Mã dịch vụ', 'Tên dịch vụ', 'Tiền', '#']
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.frame_services, text=header)
            header_label.grid(row=0, column=j, sticky="ew")
            self.frame_services.grid_columnconfigure(j, weight=1)

        self.frame_services.grid_columnconfigure(2, weight=3)
        # Populate the table with services
        for i, service in enumerate(self.list_services, start=1):
            service_id_label = ctk.CTkLabel(self.frame_services,
                                            text=service['id'])
            service_id_label.grid(row=i, column=0, sticky="ew", pady=5)

            service_name_label = ctk.CTkLabel(self.frame_services,
                                              text=service['name'])
            service_name_label.grid(row=i, column=1, sticky="ew", pady=5)

            service_price_label = ctk.CTkLabel(self.frame_services,
                                               text=service['price'])
            service_price_label.grid(row=i, column=2, sticky="ew", pady=5)

            delete_button = ctk.CTkButton(self.frame_services, text="Xóa",
                                          command=lambda s=service: self.delete_service(s), width=50, height=20)
            delete_button.grid(row=i, column=3, sticky="ew", padx=5, pady=5)

        service_total_price = ctk.CTkLabel(self.frame_services,
                                           text='Tổng tiền: ')
        service_total_price.grid(row=len(self.list_services) + 1, column=1, sticky="ew")
        service_total_price = ctk.CTkLabel(self.frame_services,
                                           text=str(self.total_price) + ' VNĐ', width=50,
                                           height=20)
        service_total_price.grid(row=len(self.list_services) + 1, column=2, sticky="ew")

    def delete_service(self, s):
        self.list_services.remove(s)
        self.total_price -= s['price']
        self.total_price_var.set(str(self.total_price) + ' VNĐ')
        self.load_services()

    def save_bill(self, appointment):
        selected_name = self.status_name_var.get()
        status = self.list_status.get(selected_name, None)
        if status is None:
            show_warning('Chọn trạng thái thanh toán')
            return
        data = [appointment.appointment_id, self.total_price, status]

        result = self.service.create_bill(data, self.list_services)

        if result:
            show_info('Lập hóa đơn thành công')
            self.parent.reload()
        else:
            show_warning('Lập hóa đơn thất bại')


class MyAppointment(ctk.CTkFrame):
    def __init__(self, parent, current_user, app=None):
        super().__init__(parent)
        self.current_user = current_user
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.app = app

        self.list_appointment = ListAppointment(self, current_user)
        self.list_appointment.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.create_bill = CreateBill(self, None)

    def load_bill(self, data):
        self.create_bill.destroy()
        self.create_bill = CreateBill(self, data)
        self.create_bill.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def reload(self):
        self.app.show_my_appointment()
