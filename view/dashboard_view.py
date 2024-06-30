import customtkinter as ctk

from service.dashboard import DashboardService


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)

        self.service = DashboardService()
        report = self.service.dashboard()

        self.label = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 20), text_color='white', width=400, height=50)
        self.label.pack(pady=20)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label = ctk.CTkLabel(self.frame, text='Thông tin tổng quan')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số bác sĩ: {report["total_doctors"]}')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số bác sĩ hiện tại: {report["total_active_doctors"]}')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số bệnh nhân: {report["total_victim"]}')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số bệnh nhân: {report["total_active_victim"]}')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số dịch vụ: {report["total_services"]}')
        self.label.pack(pady=12, padx=10)

        self.label = ctk.CTkLabel(self.frame, text=f'Tổng số lịch khám: {report["total_appointments"]}')
        self.label.pack(pady=12, padx=10)
