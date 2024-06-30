from tkinter import StringVar

import customtkinter as ctk

from service.doctor import DoctorService
from utils.alert import show_warning, show_info, show_confirm


class ListDoctorView(ctk.CTkScrollableFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.list_doctor = None
        self.pack_propagate(False)
        self.parent = app

        self.service = DoctorService()

        self.load_data()

    def load_data(self):
        # Xóa các widget hiện có trên ScrollableFrame
        for widget in self.winfo_children():
            widget.destroy()

        # Lấy dữ liệu mới
        self.list_doctor = self.service.get_doctors()
        headers = ["ID", "Full Name", "Phone", "Email", "Specialty", "Username", "Edit", "Delete"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=120, height=25)
            header_label.grid(row=0, column=j, padx=5, pady=5)

        # Hiển thị thông tin của mỗi bác sĩ trên mỗi hàng của bảng
        for i, doctor in enumerate(self.list_doctor, start=1):
            data = [doctor.doctorId, doctor.fullName, doctor.phone, doctor.email, doctor.speciality,
                    doctor.user.username]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=120, height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)

            edit_button = ctk.CTkButton(self, text="Sửa", width=70, height=25,
                                        command=lambda doc=doctor: self.edit_doctor(doc))
            edit_button.grid(row=i, column=len(data), padx=5, pady=5)

            delete_button = ctk.CTkButton(self, text="Xóa", width=70, height=25, bg_color='red',
                                          fg_color='transparent', hover_color='dark red',
                                          command=lambda doc=doctor: self.delete_doctor(doc))
            delete_button.grid(row=i, column=len(data) + 1, padx=5, pady=5)

    def edit_doctor(self, doc):
        self.parent.switch_tab('Thêm bác sĩ', doc)

    def delete_doctor(self, doc):
        msg = "Bạn có chắc chắn muốn xóa bác sĩ này?"
        if show_confirm(msg):
            result = self.service.delete_doctor(doc.doctorId)
            if result:
                message = "Xóa bác sĩ thành công"
                show_info(message)
                self.load_data()
            else:
                message = "Xóa bác sĩ thất bại"
                show_warning(message)


class AddDoctorView(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.pack_propagate(False)

        self.is_add = False
        self.parent = app

        self.doctor_id = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.full_name_var = StringVar()
        self.specialty_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()

        self.frame = ctk.CTkFrame(master=self, width=400, )
        self.frame.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.label_info = ctk.CTkLabel(master=self.frame, text='Thông tin bác sĩ', font=("Arial", 16))
        self.label_info.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

        # Tên đăng nhập
        self.lb_username = ctk.CTkLabel(master=self.frame, text='Tên đăng nhập')
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

        # Email
        self.lb_email = ctk.CTkLabel(master=self.frame, text='Email')
        self.lb_email.grid(row=5, column=0, pady=2, padx=2, sticky="e")
        self.email = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập email", width=250,
                                  textvariable=self.email_var)
        self.email.grid(row=5, column=1, pady=12, padx=10)

        # Chuyên khoa
        self.lb_specialty = ctk.CTkLabel(master=self.frame, text='Chuyên khoa')
        self.lb_specialty.grid(row=6, column=0, pady=2, padx=2, sticky="e")
        self.specialty = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập chuyên khoa", width=250,
                                      textvariable=self.specialty_var)
        self.specialty.grid(row=6, column=1, pady=12, padx=10)

        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm bác sĩ'
        self.button = ctk.CTkButton(master=self.frame, text=txt_btn, command=self.action)
        self.button.grid(row=9, column=0, columnspan=2, pady=12, padx=10)

        self.service = DoctorService()

    def reset_form(self):
        if self.is_add:
            self.parent.refresh_v2()
        else:
            self.username_var.set('')
            self.password_var.set('')
            self.full_name_var.set('')
            self.phone_var.set('')
            self.email_var.set('')
            self.specialty_var.set('')
            self.doctor_id.set('')
            self.is_add = False

    def switch_mode(self):
        self.is_add = not self.is_add
        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm bác sĩ'
        self.button.configure(text=txt_btn)

    def fill_data(self, doc):
        if doc:
            self.doctor_id.set(doc.doctorId)
            if doc.user.username:
                self.username_var.set(doc.user.username)
            if doc.fullName:
                self.full_name_var.set(doc.fullName)
            if doc.phone:
                self.phone_var.set(doc.phone)
            if doc.email:
                self.email_var.set(doc.email)
            if doc.speciality:
                self.specialty_var.set(doc.speciality)

        self.username.configure(state='disabled')

    def action(self):
        data = [self.username.get(), self.password.get(), self.full_name.get(), self.phone.get(), self.email_var.get(),
                self.specialty_var.get()]

        # validate data
        if not all(data) and not self.is_add:
            message = "Vui lòng nhập đầy đủ thông tin"
            show_warning(message)
            return
        elif self.is_add:
            # check all data is valid except password
            if not all(data[2:]):
                message = "Vui lòng nhập đầy đủ thông tin"
                show_warning(message)
                return

        if self.is_add:
            if data[1] != '':
                self.service.update_password(data[0], data[1])
            data1 = [data[2], data[5], data[4], data[3], self.doctor_id.get()]
            # update victim
            result = self.service.update_doctor(data1)

            if result:
                message = "Cập nhật bác sĩ thành công"
                show_info(message)
            else:
                message = "Cập nhật bác sĩ thất bại"
                show_warning(message)
        else:
            data1 = [data[0], data[1], data[2], data[5], data[4], data[3]]
            # add victim
            result = self.service.add_doctor(data1)

            if result:
                message = "Thêm bác sĩ thành công"
                show_info(message)
            else:
                message = "Thêm bác sĩ thất bại"
                show_warning(message)

        self.reset_form()


class DoctorListGUI(ctk.CTkTabview):
    def __init__(self, parent, user, app):
        super().__init__(parent)
        self.pack_propagate(False)

        self.user = user
        self.app = app

        self.add('Danh sách bác sĩ')
        self.add('Thêm bác sĩ')

        self.list_view = ListDoctorView(self.tab('Danh sách bác sĩ'), app=self)
        self.list_view.pack(fill='both', expand=True)

        self.add_view = AddDoctorView(self.tab('Thêm bác sĩ'), self)
        self.add_view.pack(fill='both', expand=True)

    def switch_tab(self, tab, doc=None):
        if tab == 'Thêm bác sĩ':
            self.add_view.switch_mode()
            if doc:
                self.add_view.fill_data(doc)
        self.set(tab)

    def refresh(self):
        self.list_view.destroy()
        self.list_view = ListDoctorView(self.tab('Danh sách bác sĩ'), app=self)
        self.list_view.pack(fill='both', expand=True)
        self.set('Danh sách bác sĩ')

    def refresh_v2(self):
        self.app.show_doctor_list()
