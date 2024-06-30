from tkinter import StringVar

import customtkinter as ctk

from service.service import ServiceService
from utils.alert import show_confirm, show_info, show_warning


class ListServiceView(ctk.CTkScrollableFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.list_service = None
        self.pack_propagate(False)
        self.parent = app
        self.configure()

        self.service = ServiceService()
        self.load_data()

    def load_data(self):
        # Xóa các widget hiện có trên ScrollableFrame
        for widget in self.winfo_children():
            widget.destroy()

        # Lấy dữ liệu mới
        self.list_service = self.service.get_services()
        headers = ["ID", "Service name", "Description", "Price", "Edit", "Delete"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=120, height=25)
            header_label.grid(row=0, column=j, padx=5, pady=5)

        # Hiển thị thông tin của mỗi dịch vụ trên mỗi hàng của bảng
        for i, s in enumerate(self.list_service, start=1):
            data = [s.service_id, s.service_name, s.description, s.price]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=120, height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)

            edit_button = ctk.CTkButton(self, text="Sửa", width=70, height=25,
                                        command=lambda doc=s: self.edit_service(doc))
            edit_button.grid(row=i, column=len(data), padx=5, pady=5)

            delete_button = ctk.CTkButton(self, text="Xóa", width=70, height=25, bg_color='red',
                                          fg_color='transparent', hover_color='dark red',
                                          command=lambda doc=s: self.delete_service(doc))
            delete_button.grid(row=i, column=len(data) + 1, padx=5, pady=5)

    def edit_service(self, doc):
        self.parent.switch_tab('Thêm dịch vụ', doc)

    def delete_service(self, doc):
        msg = "Bạn có chắc chắn muốn xóa dịch vụ này?"
        if show_confirm(msg):
            result = self.service.delete_services(doc.service_id)
            if result:
                message = "Xóa dịch vụ thành công"
                show_info(message)
                self.load_data()
            else:
                message = "Xóa dịch vụ thất bại"
                show_warning(message)


class AddServiceView(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.pack_propagate(False)
        self.configure()
        self.is_add = False
        self.parent = app

        self.service_id = StringVar()
        self.service_name_var = StringVar()
        self.description_var = StringVar()
        self.price_var = StringVar()

        self.frame = ctk.CTkFrame(master=self, width=400, )
        self.frame.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.label_info = ctk.CTkLabel(master=self.frame, text='Thông tin dịch vụ', font=("Arial", 16))
        self.label_info.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

        # Tên dịch vụ
        self.lb_service_name = ctk.CTkLabel(master=self.frame, text='Tên dịch vụ')
        self.lb_service_name.grid(row=1, column=0, pady=2, padx=2, sticky="e")
        self.service_name = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập tên dịch vụ", width=250,
                                         textvariable=self.service_name_var)
        self.service_name.grid(row=1, column=1, pady=12, padx=10)

        # Mô tả
        self.lb_description = ctk.CTkLabel(master=self.frame, text='Mô tả')
        self.lb_description.grid(row=2, column=0, pady=2, padx=2, sticky="e")
        self.description = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập mô tả", width=250,
                                        textvariable=self.description_var)
        self.description.grid(row=2, column=1, pady=12, padx=10)

        # Giá
        self.lb_price = ctk.CTkLabel(master=self.frame, text='Giá')
        self.lb_price.grid(row=3, column=0, pady=2, padx=2, sticky="e")
        self.price = ctk.CTkEntry(master=self.frame, placeholder_text="Nhập giá", width=250,
                                  textvariable=self.price_var)
        self.price.grid(row=3, column=1, pady=12, padx=10)

        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm dịch vụ'
        self.button = ctk.CTkButton(master=self.frame, text=txt_btn, command=self.action)
        self.button.grid(row=9, column=0, columnspan=2, pady=12, padx=10)

        self.service = ServiceService()

    def reset_form(self):
        if self.is_add:
            self.parent.refresh()
        else:
            self.service_name_var.set('')
            self.description_var.set('')
            self.price_var.set('')
            self.service_id.set('')

    def switch_mode(self):
        self.is_add = not self.is_add
        txt_btn = 'Cập nhật thông tin' if self.is_add else 'Thêm dịch vụ'
        self.button.configure(text=txt_btn)

    def fill_data(self, doc):
        if doc:
            self.service_id.set(doc.service_id)
            if doc.service_name:
                self.service_name_var.set(doc.service_name)
            if doc.description:
                self.description_var.set(doc.description)
            if doc.price:
                self.price_var.set(doc.price)

    def action(self):
        data = [self.service_name_var.get(), self.description_var.get(), self.price_var.get()]

        # validate dataD
        if not all(data) and not self.is_add:
            message = "Vui lòng nhập đầy đủ thông tin"
            show_warning(message)
            return

        if self.is_add:
            data1 = [data[0], data[1], data[2], self.service_id.get()]
            # update victim
            result = self.service.update_services(data1)

            if result:
                message = "Cập nhật dịch vụ thành công"
                show_info(message)
            else:
                message = "Cập nhật dịch vụ thất bại"
                show_warning(message)
        else:
            data1 = [data[0], data[1], data[2]]
            # add victim
            result = self.service.add_services(data1)

            if result:
                message = "Thêm dịch vụ thành công"
                show_info(message)
            else:
                message = "Thêm dịch vụ thất bại"
                show_warning(message)

        self.reset_form()


class ServiceListGUI(ctk.CTkTabview):
    def __init__(self, parent, user, app):
        super().__init__(parent)
        self.pack_propagate(False)
        self.configure()

        self.user = user
        self.app = app

        self.add('Danh sách dịch vụ')
        self.add('Thêm dịch vụ')

        self.list_view = ListServiceView(self.tab('Danh sách dịch vụ'), app=self)
        self.list_view.pack(fill='both', expand=True)

        self.add_view = AddServiceView(self.tab('Thêm dịch vụ'), app=self)
        self.add_view.pack(fill='both', expand=True)

    def switch_tab(self, tab, doc=None):
        if tab == 'Thêm dịch vụ':
            self.add_view.switch_mode()
            if doc:
                self.add_view.fill_data(doc)
        self.set(tab)

    def refresh(self):
        self.app.show_service_list()
