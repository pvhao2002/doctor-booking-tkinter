from tkinter import Tk

import customtkinter as ctk

from sidebar import Sidebar
from view.login_view import LoginPage
from view.booking_view import BookingView
from view.dashboard_view import Dashboard
from view.doctor_view import DoctorListGUI
from view.invoice_view import ListInvoiceView
from view.my_appointment_view import MyAppointment
from view.my_booking_view import HistoryView
from view.victim_view import VictimListView
from view.profile_view import ProfileView
from view.service_view import ServiceListGUI


class MainApp(ctk.CTk):
    def __init__(self, mUser=None):
        super().__init__()
        self.list_bill = None
        self.my_history = None
        self.booking = None
        self.profile = None
        self.service_list = None
        self.victim_list = None
        self.dashboard = None
        self.doctor_list = None

        self.title("App quản lý đặt lịch khám bệnh")
        self.geometry("1280x700+200+50")
        self.resizable(False, False)
        self.maxsize(1280, 700)
        self.user = mUser
        self.container = ctk.CTkFrame(master=self)
        self.container.pack(fill='both', expand=True)

        self.sidebar = Sidebar(self.container, self.user, self)
        self.sidebar.pack(side='left', fill='y')

        if self.user is not None:
            print(self.user.role)
            if self.user.role == 'admin':
                self.dashboard = Dashboard(self.container)
                self.dashboard.pack(side='right', fill='both', expand=True)
            elif self.user.role == 'doctor':
                self.my_appointment = MyAppointment(self.container, self.user, self)
                self.my_appointment.pack(side='right', fill='both', expand=True)
            else:
                self.victim_list = ProfileView(self.container, self.user)
                self.victim_list.pack(side='right', fill='both', expand=True)

    def init_view(self):
        if self.user is not None:
            if self.user.role == 'admin':
                self.dashboard = Dashboard(self.container)
                self.dashboard.pack(side='right', fill='both', expand=True)
            elif self.user.role == 'doctor':
                self.my_appointment = MyAppointment(self.container, self.user, self)
                self.my_appointment.pack(side='right', fill='both', expand=True)
            else:
                self.booking = BookingView(self.container, self.user)
                self.booking.pack(side='right', fill='both', expand=True)

    def run(self):
        self.mainloop()

    def destroy_children(self):
        for widget in self.container.winfo_children():
            # remove all children except the sidebar
            if widget != self.sidebar:
                widget.destroy()

    def refresh(self):
        self.sidebar.destroy()
        self.sidebar = Sidebar(self.container, self.user, self)
        self.sidebar.pack(side='left', fill='y')

    def show_doctor_list(self):
        self.destroy_children()
        self.doctor_list = DoctorListGUI(self.container, self.user, self)
        self.doctor_list.pack(side='right', fill='both', expand=True)

    def show_home(self):
        self.destroy_children()
        self.dashboard = Dashboard(self.container)
        self.dashboard.pack(side='right', fill='both', expand=True)

    def show_victim_list(self):
        self.destroy_children()
        self.victim_list = VictimListView(self.container, self.user, self)
        self.victim_list.pack(side='right', fill='both', expand=True)

    def show_service_list(self):
        self.destroy_children()
        self.service_list = ServiceListGUI(self.container, self.user, self)
        self.service_list.pack(side='right', fill='both', expand=True)

    def show_history(self):
        self.destroy_children()
        self.my_history = HistoryView(self.container, self.user)
        self.my_history.pack(side='right', fill='both', expand=True)

    def show_profile(self):
        self.destroy_children()
        self.profile = ProfileView(self.container, self.user)
        self.profile.pack(side='right', fill='both', expand=True)

    def show_booking(self):
        self.destroy_children()
        self.booking = BookingView(self.container, self.user)
        self.booking.pack(side='right', fill='both', expand=True)

    def show_my_appointment(self):
        self.destroy_children()
        self.my_appointment = MyAppointment(self.container, self.user, self)
        self.my_appointment.pack(side='right', fill='both', expand=True)

    def show_list_bill(self):
        self.destroy_children()
        self.list_bill = ListInvoiceView(self.container, self.user)
        self.list_bill.pack(side='right', fill='both', expand=True)


if __name__ == "__main__":
    window = Tk()
    login = LoginPage(window)
    window.mainloop()
    current_user = login.get_current_user()
    if current_user is not None:
        app = MainApp(current_user)
        app.run()
    # app = MainApp(current_user)
    # login = LoginGUI(current_user=current_user, app=app)
    # login.run()
