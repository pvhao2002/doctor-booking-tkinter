from datetime import datetime
from tkinter import StringVar, IntVar

import customtkinter as ctk
from tkcalendar import DateEntry

from service.victim import VictimService
from utils.alert import show_confirm, show_warning, show_info


class ListVictimView(ctk.CTkScrollableFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.list_victims = None
        self.pack_propagate(False)

        self.parent = app
        self.service = VictimService()

        self.load_data()

    def edit_victim(self, doc):
        self.parent.switch_tab('Thêm bệnh nhân', doc)

    def delete_victim(self, doc):
        msg = "Bạn có chắc chắn muốn xóa bệnh nhân này?"
        if show_confirm(msg):
            result = self.service.delete_victims(doc.victimId)
            if result:
                message = "Xóa bệnh nhân thành công"
                show_info(message)
                self.load_data()
            else:
                message = "Xóa bệnh nhân thất bại"
                show_warning(message)

    def load_data(self):
        # Xóa các widget hiện có trên ScrollableFrame
        for widget in self.winfo_children():
            widget.destroy()

        # Lấy dữ liệu mới
        self.list_victims = self.service.get_victims()
        headers = ["ID", "Username", "Full Name", "Gender", "Birthday", "Address", "Phone", "Age", "Edit", "Delete"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=70, height=25)
            header_label.grid(row=0, column=j, padx=5, pady=5)

        for i, victim in enumerate(self.list_victims, start=1):
            data = [victim.victimId, victim.user.username, victim.fullName, victim.gender, victim.birthDate,
                    victim.address, victim.phone, victim.age]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=70, height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)

            edit_button = ctk.CTkButton(self, text="Sửa", width=70, height=25,
                                        command=lambda doc=victim: self.edit_victim(doc))
            edit_button.grid(row=i, column=len(data), padx=5, pady=5)

            delete_button = ctk.CTkButton(self, text="Xóa", width=70, height=25, bg_color='red',
                                          fg_color='transparent', hover_color='dark red',
                                          command=lambda doc=victim: self.delete_victim(doc))
            delete_button.grid(row=i, column=len(data) + 1, padx=5, pady=5)


class AddVictimView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)

        self.is_add = False

        self.victim_id = IntVar()
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.full_name_var = StringVar()
        self.address_var = StringVar()
        self.age_var = StringVar()
        self.phone_var = StringVar()

        self.frame = ctk.CTkFrame(master=self, width=400, )
        self.frame.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.label_info = ctk.CTkLabel(master=self.frame, text='Thông tin bệnh nhân', font=("Arial", 16))
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

        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm bệnh nhân'
        self.button = ctk.CTkButton(master=self.frame, text=txt_btn, command=self.action)
        self.button.grid(row=9, column=0, columnspan=2, pady=12, padx=10)

        self.service = VictimService()

    def reset_form(self):
        self.username_var.set('')
        self.password_var.set('')
        self.full_name_var.set('')
        self.phone_var.set('')
        self.is_add = False
        self.switch_mode()
        self.address.delete('1.0', ctk.END)

    def get_gender(self):
        if self.gender_var.get() == 'Nam':
            return 'MALE'
        elif self.gender_var.get() == 'Nữ':
            return 'FEMALE'
        else:
            return 'OTHER'

    def switch_mode(self):
        self.is_add = not self.is_add
        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm bệnh nhân'
        self.button.configure(text=txt_btn)

    def fill_data(self, doc):
        if doc:
            self.victim_id.set(doc.victimId)
            if doc.user.username:
                self.username_var.set(doc.user.username)
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

    def action(self):
        birthday_str = self.birthday.get()
        birthday = datetime.strptime(birthday_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        data = [self.username.get(), self.password.get(), self.full_name.get(), self.get_gender(),
                birthday, self.address.get("1.0", "end-1c"), self.phone.get(), self.age.get()]

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

            data1 = [data[2], data[3], data[4], data[5], data[6], data[7], self.victim_id.get()]
            # update victim
            result = self.service.update_victims(data1)

            if result:
                message = "Cập nhật bệnh nhân thành công"
                show_info(message)
            else:
                message = "Cập nhật bệnh nhân thất bại"
                show_warning(message)
        else:
            data1 = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]]
            # add victim
            result = self.service.add_victims(data1)

            if result:
                message = "Thêm bệnh nhân thành công"
                show_info(message)
            else:
                message = "Thêm bệnh nhân thất bại"
                show_warning(message)

        self.reset_form()


class VictimListView(ctk.CTkTabview):
    def __init__(self, parent, user, app):
        super().__init__(parent)
        self.pack_propagate(False)

        self.user = user
        self.app = app

        self.add('Danh sách bệnh nhân')
        self.add('Thêm bệnh nhân')

        self.list_view = ListVictimView(self.tab('Danh sách bệnh nhân'), app=self)
        self.list_view.pack(fill='both', expand=True)

        self.add_view = AddVictimView(self.tab('Thêm bệnh nhân'))
        self.add_view.pack(fill='both', expand=True)

    def switch_tab(self, tab, doc=None):
        if tab == 'Thêm bệnh nhân':
            self.add_view.switch_mode()
            if doc:
                self.add_view.fill_data(doc)
        self.set(tab)

    def refresh(self):
        self.list_view.destroy()
        self.list_view = ListVictimView(self.tab('Danh sách bệnh nhân'), app=self)
        self.list_view.pack(fill='both', expand=True)
        self.set('Danh sách bệnh nhân')
