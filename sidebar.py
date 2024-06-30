import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, user, app):
        super().__init__(parent)
        self.pack_propagate(False)
        self.configure(width=200, bg_color="light sky blue", fg_color='transparent')

        self.user = user
        self.app = app

        button_bg = "dodger blue"
        button_fg = "black"

        # Thêm các nút hoặc các thành phần khác vào sidebar
        if user:
            if user.role == 'admin':
                self.button1 = ctk.CTkButton(self, text="Trang chủ", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('home'))
                self.button1.pack(pady=10, fill=ctk.X)

                self.button2 = ctk.CTkButton(self, text="Quản lý bệnh nhân", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('victim'))
                self.button2.pack(pady=10, fill=ctk.X)

                self.button3 = ctk.CTkButton(self, text="Quản lý bác sĩ", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('doctor'))
                self.button3.pack(pady=10, fill=ctk.X)

                self.button4 = ctk.CTkButton(self, text="Quản lý dịch vụ giá", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('service'))
                self.button4.pack(pady=10, fill=ctk.X)

                self.button5 = ctk.CTkButton(self, text="Quản lý hóa đơn", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('bill'))
                self.button5.pack(pady=10, fill=ctk.X)

            elif user.role == 'doctor':
                self.button7 = ctk.CTkButton(self, text="Lập hóa đơn", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('create_bill'))
                self.button7.pack(pady=10, fill=ctk.X)

            else:
                self.button6 = ctk.CTkButton(self, text="Đặt lịch", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('booking'))
                self.button6.pack(pady=10, fill=ctk.X)

                self.button8 = ctk.CTkButton(self, text="Lịch sử đặt lịch", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('history'))
                self.button8.pack(pady=10, fill=ctk.X)

                self.button9 = ctk.CTkButton(self, text="Thông tin cá nhân", bg_color=button_bg, text_color=button_fg,
                                             fg_color='transparent', border_color='cyan4', border_width=2,
                                             command=lambda: self.open_tab('profile'))
                self.button9.pack(pady=10, fill=ctk.X)

        self.button91 = ctk.CTkButton(self, text="Thoát", bg_color=button_bg, text_color=button_fg,
                                      fg_color='transparent', border_color='cyan4', border_width=2,
                                      command=lambda: self.open_tab('exit'))
        self.button91.pack(pady=10, fill=ctk.X, side='bottom')

    def open_tab(self, tab):
        if tab == 'home':
            self.app.show_home()
        elif tab == 'victim':
            self.app.show_victim_list()
        elif tab == 'doctor':
            self.app.show_doctor_list()
        elif tab == 'service':
            self.app.show_service_list()
        elif tab == 'bill':
            self.app.show_list_bill()
        elif tab == 'create_bill':
            self.app.show_my_appointment()
        elif tab == 'history':
            self.app.show_history()
        elif tab == 'profile':
            self.app.show_profile()
        elif tab == 'booking':
            self.app.show_booking()
        elif tab == 'exit':
            self.app.destroy_children()
            self.app.destroy()
            exit(0)
