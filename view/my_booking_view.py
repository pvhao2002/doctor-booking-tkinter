import customtkinter as ctk

from dto.invoice_detail import InvoiceDetail
from service.booking import BookingService
from service.victim import VictimService
from utils.alert import show_warning


def get_status(status):
    if status == 'pending':
        return 'Đang chờ'
    if status == 'accepted':
        return 'Đã chấp nhận'
    if status == 'cancelled':
        return 'Đã hủy'
    if status == 'completed':
        return 'Đã hoàn thành'
    return 'Không xác định'


class MyBookingView(ctk.CTkScrollableFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.pack_propagate(False)
        self.service = BookingService()
        self.current_user = current_user
        self.victim_service = VictimService()
        self.info = self.victim_service.get_info(current_user.id)
        self.parent = parent
        self.load_data()

    def load_data(self):
        # destroy all widgets
        for widget in self.winfo_children():
            widget.destroy()

        list_booking = self.service.get_appointment(self.info.victimId)

        headers = ["Mã đặt", "Mã bác sĩ", "Tên bác sĩ", "Ngày đặt", "Trạng thái", "#"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=70, height=25)
            header_label.grid(row=0, column=j, padx=5, pady=5)

        for i, b in enumerate(list_booking, start=1):
            data = [b.appointment_id, b.doctor.doctorId, b.doctor.fullName, b.appointment_date, get_status(b.status)]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=70,
                                          height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)

            if b.status == 'pending':
                cancel_button = ctk.CTkButton(self, text="Hủy", width=70, height=25, bg_color='red',
                                              fg_color='transparent', hover_color='dark red',
                                              command=lambda doc=b: self.cancel_booking(doc))
                cancel_button.grid(row=i, column=len(data), padx=5, pady=5)

            if b.status == 'completed':
                see_button = ctk.CTkButton(self, text="Xem chi tiết", width=70, height=25,
                                           command=lambda doc=b: self.detail_booking(doc))
                see_button.grid(row=i, column=len(data), padx=5, pady=5)

    def detail_booking(self, doc):
        self.parent.load_history(doc.appointment_id)

    def cancel_booking(self, doc):
        result = self.service.update_status_appointment(doc.appointment_id, 'cancelled')
        if result:
            self.load_data()
        else:
            msg = 'Hủy đặt lịch thất bại'
            show_warning(msg)


class DetailBooking(ctk.CTkScrollableFrame):
    def __init__(self, parent, appointment_id=None):
        super().__init__(parent, border_color='black', border_width=1, corner_radius=5)
        self.pack_propagate(False)
        self.configure()
        self.service = BookingService()
        if appointment_id:
            self.load_data(appointment_id)

    def load_data(self, appointment_id):
        detail_invoice = self.service.get_invoice(appointment_id)
        invoice_dto = InvoiceDetail(detail_invoice)
        i = 0

        lb_invoice_id = ctk.CTkLabel(master=self, text=f"Mã hóa đơn: {invoice_dto.invoice_id}")
        lb_invoice_id.grid(row=i, column=0, padx=5, pady=5)
        i += 1

        lb_total_amount = ctk.CTkLabel(master=self, text=f"Tổng tiền: {invoice_dto.total_amount}")
        lb_total_amount.grid(row=i, column=0, padx=5, pady=5)
        i += 1

        lb_create_date = ctk.CTkLabel(master=self, text=f"Ngày tạo: {invoice_dto.create_date}")
        lb_create_date.grid(row=i, column=0, padx=5, pady=5)
        i += 1

        lb_payment_status = ctk.CTkLabel(master=self, text=f"Trạng thái thanh toán: {invoice_dto.payment_status}")
        lb_payment_status.grid(row=i, column=0, padx=5, pady=5)
        i += 1

        headers = ["Mã dịch vụ", "Tên dịch vụ", "Giá"]
        for j, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, width=70,
                                        height=25)
            header_label.grid(row=4, column=j, padx=5, pady=5)

        for i, service in enumerate(invoice_dto.list_service, start=5):
            data = [service.service_id, service.service_name, service.price]
            for j, value in enumerate(data):
                cell_label = ctk.CTkLabel(self, text=value, width=70,
                                          height=25)
                cell_label.grid(row=i, column=j, padx=5, pady=5)


class HistoryView(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.pack_propagate(False)
        self.service = BookingService()
        self.current_user = current_user
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.list_booking = MyBookingView(self, current_user)
        self.list_booking.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.detail_booking = []
        self.history = DetailBooking(self, None)

    def load_history(self, data):
        self.history.destroy()
        self.history = DetailBooking(self, data)
        self.history.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
