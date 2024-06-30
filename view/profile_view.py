from datetime import datetime
from tkinter import StringVar, IntVar

import customtkinter as ctk
from tkcalendar import DateEntry

from service.victim import VictimService
from utils.alert import show_warning, show_info


class ProfileView(ctk.CTkFrame):
    def __init__(self, parent, info=None):
        super().__init__(parent)
        self.info = info
        self.pack_propagate(False)
        self.service = VictimService()

        self.victim_id = IntVar()
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.full_name_var = StringVar()
        self.address_var = StringVar()
        self.age_var = StringVar()
        self.phone_var = StringVar()

        self.frame = ctk.CTkFrame(master=self, width=400)
        self.frame.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.label_info = ctk.CTkLabel(master=self.frame,
                                       text='Thông tin cá nhân', font=("Arial", 16))
        self.label_info.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

        # Tên đăng nhập
        self.lb_username = ctk.CTkLabel(master=self.frame,
                                        text='Tên đăng nhập')
        self.lb_username.grid(row=1, column=0, pady=2, padx=2, sticky="e")
        self.username = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập tên đăng nhập", width=250,
                                     textvariable=self.username_var)
        self.username.grid(row=1, column=1, pady=12, padx=10)

        # Mật khẩu
        self.lb_password = ctk.CTkLabel(master=self.frame, text='Mật khẩu')
        self.lb_password.grid(row=2, column=0, pady=2, padx=2, sticky="e")
        self.password = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập mật khẩu", width=250,
                                     textvariable=self.password_var)
        self.password.grid(row=2, column=1, pady=12, padx=10)

        # Họ và tên
        self.lb_full_name = ctk.CTkLabel(master=self.frame, text='Họ và tên')
        self.lb_full_name.grid(row=3, column=0, pady=2, padx=2, sticky="e")
        self.full_name = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập họ và tên", width=250,
                                      textvariable=self.full_name_var)
        self.full_name.grid(row=3, column=1, pady=12, padx=10)

        # Số điện thoại
        self.lb_phone = ctk.CTkLabel(master=self.frame, text='Số điện thoại')
        self.lb_phone.grid(row=4, column=0, pady=2, padx=2, sticky="e")
        self.phone = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập số điện thoại", width=250,
                                  textvariable=self.phone_var)
        self.phone.grid(row=4, column=1, pady=12, padx=10)

        # Giới tính
        self.lb_gender = ctk.CTkLabel(master=self.frame, text='Giới tính')
        self.lb_gender.grid(row=5, column=0, pady=2, padx=2, sticky="e")
        self.gender_var = ctk.StringVar(value='Nam')
        self.gender_selection = ctk.CTkComboBox(master=self.frame, values=['Nam', 'Nữ', 'Khác'],
                                                variable=self.gender_var, width=250)
        self.gender_selection.grid(row=5, column=1, pady=12, padx=10)

        # Ngày sinh
        self.lb_birthday = ctk.CTkLabel(master=self.frame, text='Ngày sinh')
        self.lb_birthday.grid(row=6, column=0, pady=2, padx=2, sticky="e")
        self.birthday = DateEntry(master=self.frame, width=30, background='darkblue', foreground='white',
                                  borderwidth=2, font=("Arial", 14), date_pattern='dd-MM-yyyy')
        self.birthday.grid(row=6, column=1, pady=12, padx=10)

        # Địa chỉ
        self.lb_address = ctk.CTkLabel(master=self.frame, text='Địa chỉ')
        self.lb_address.grid(row=7, column=0, pady=2, padx=2, sticky="ne")
        self.address = ctk.CTkTextbox(master=self.frame, height=100, width=250, )
        self.address.grid(row=7, column=1, pady=12, padx=10, sticky="we")

        # Tuổi
        self.lb_age = ctk.CTkLabel(master=self.frame, text='Tuổi')
        self.lb_age.grid(row=8, column=0, pady=2, padx=2, sticky="e")
        self.age = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập tuổi", width=250, textvariable=self.age_var)
        self.age.grid(row=8, column=1, pady=12, padx=10)

        txt_btn = 'Cập nhật thông tin'
        self.button = ctk.CTkButton(master=self.frame, text=txt_btn, command=self.action)
        self.button.grid(row=9, column=0, columnspan=2, pady=12, padx=10)

        self.fill_data()

    def action(self):
        birthday_str = self.birthday.get()
        birthday = datetime.strptime(birthday_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        data = [self.username.get(), self.password.get(), self.full_name.get(), self.get_gender(),
                birthday, self.address.get("1.0", "end-1c"), self.phone.get(), self.age.get()]
        if not all(data):
            message = "Vui lòng nhập đầy đủ thông tin"
            show_warning(message)
            return
        self.service.update_password(data[0], data[1])
        data1 = [data[2], data[3], data[4], data[5], data[6], data[7], self.victim_id.get()]
        # update victim
        result = self.service.update_victims(data1)
        if result:
            message = "Cập nhật thông tin thành công"
            show_info(message)
        else:
            message = "Cập nhật thông tin thất bại"
            show_warning(message)

    def get_gender(self):
        if self.gender_var.get() == 'Nam':
            return 'MALE'
        elif self.gender_var.get() == 'Nữ':
            return 'FEMALE'
        else:
            return 'OTHER'

    def get_victim(self):
        info = self.service.get_info(self.info.id)
        return info

    def fill_data(self):
        doc = self.get_victim()
        if doc:
            self.victim_id.set(doc.victimId)
            if doc.user.username:
                self.username_var.set(doc.user.username)
            if doc.user.password:
                self.password_var.set(doc.user.password)
            if doc.fullName:
                self.full_name_var.set(doc.fullName)
            if doc.age is not None:
                self.age_var.set(doc.age)
            if doc.phone:
                self.phone_var.set(doc.phone)
            if doc.birthDate:
                self.birthday.set_date(doc.birthDate)  # Cập nhật DateEntry
            if doc.gender:
                self.gender_var.set(doc.gender)
            if doc.address:
                self.address.delete('1.0', ctk.END)  # Xóa nội dung hiện tại
                self.address.insert('1.0', doc.address)  # Thêm nội dung mới
        self.username.configure(state='disabled')
