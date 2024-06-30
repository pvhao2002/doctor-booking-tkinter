from datetime import datetime

import customtkinter as ctk
from tkcalendar import DateEntry

from service.booking import BookingService
from service.doctor import DoctorService
from service.victim import VictimService
from utils.alert import show_info, show_warning


class BookingView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.pack_propagate(False)
        self.user = user
        doctor_service = DoctorService()
        self.frame = ctk.CTkFrame(self, width=400)
        self.frame.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.label_info = ctk.CTkLabel(self.frame, text='Đặt lịch khám bệnh', font=("Arial", 16))
        self.label_info.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

        # Bác sĩ
        list_doctor = doctor_service.get_doctors()
        self.doctor_name_to_id = {doctor.fullName: doctor.doctorId for doctor in list_doctor}

        list_doctor_name = list(self.doctor_name_to_id.keys())

        self.lb_doctor_name = ctk.CTkLabel(self.frame, text='Bác sĩ')
        self.lb_doctor_name.grid(row=5, column=0, pady=2, padx=2, sticky="e")
        self.doctor_name_var = ctk.StringVar(value='Chọn bác sĩ')
        self.doctor_name_selection = ctk.CTkComboBox(master=self.frame, values=list_doctor_name,
                                                     variable=self.doctor_name_var, width=250)
        self.doctor_name_selection.grid(row=5, column=1, pady=12, padx=10)

        # Ngày khám bệnh
        self.lb_booking_date = ctk.CTkLabel(self.frame, text='Ngày sinh')
        self.lb_booking_date.grid(row=6, column=0, pady=2, padx=2, sticky="e")
        self.booking_date = DateEntry(master=self.frame, width=30, background='darkblue', foreground='white',
                                      borderwidth=2, font=("Arial", 14), date_pattern='dd-MM-yyyy')
        self.booking_date.grid(row=6, column=1, pady=12, padx=10)

        txt_btn = 'Đặt lịch'
        self.button = ctk.CTkButton(self.frame, text=txt_btn, command=self.action)
        self.button.grid(row=9, column=0, columnspan=2, pady=12, padx=10)

        self.service = BookingService()
        self.victim_service = VictimService()

    def action(self):
        selected_name = self.doctor_name_var.get()
        doctor_id = self.doctor_name_to_id.get(selected_name, None)
        if doctor_id is not None:
            booking_date_str = self.booking_date.get()
            booking_date = datetime.strptime(booking_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            if booking_date < datetime.now().strftime("%Y-%m-%d"):
                show_warning("Ngày đặt lịch không được nhỏ hơn ngày hiện tại")
                return
            info = self.victim_service.get_info(self.user.id)
            data = [info.victimId, doctor_id, booking_date]
            result = self.service.book_appointment(data)
            if result:
                show_info("Đặt lịch thành công")
            else:
                show_warning("Đặt lịch thất bại")
        else:
            show_warning("Vui lòng chọn bác sĩ")
