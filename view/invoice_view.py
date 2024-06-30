import customtkinter as ctk

from service.booking import BookingService


class ListInvoiceView(ctk.CTkScrollableFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.list = None
        self.pack_propagate(False)
        self.parent = app

        self.service = BookingService()

        self.load_data()

    def load_data(self):
        # Xóa các widget hiện có trên ScrollableFrame
        for widget in self.winfo_children():
            widget.destroy()

        # Lấy dữ liệu mới
        self.list = self.service.get_all_invoice()
        index_row = 0
        # Hiển thị thông tin của mỗi dịch vụ trên mỗi hàng của bảng
        for i, s in enumerate(self.list, start=0):
            dash = ''
            for _ in range(180):
                dash += '-'

            lb_dash = ctk.CTkLabel(self, text=dash, width=70, height=25)
            lb_dash.grid(row=index_row, column=0, padx=5, pady=5)
            index_row += 1

            lb_invoice_id = ctk.CTkLabel(self,
                                         text=f"Mã hóa đơn: {s.invoice_id}", width=70, height=25)
            lb_invoice_id.grid(row=index_row, column=0, padx=5, pady=5)
            index_row += 1
            lb_total_amount = ctk.CTkLabel(self,
                                           text=f"Tổng tiền: {s.total_amount}", width=70, height=25)
            lb_total_amount.grid(row=index_row, column=0, padx=5, pady=5)
            index_row += 1
            lb_create_date = ctk.CTkLabel(self,
                                          text=f"Ngày tạo: {s.create_date}", width=70, height=25)
            lb_create_date.grid(row=index_row, column=0, padx=5, pady=5)
            index_row += 1
            lb_payment_status = ctk.CTkLabel(self,
                                             text=f"Trạng thái thanh toán: {s.payment_status}", width=70,
                                             height=25)
            lb_payment_status.grid(row=index_row, column=0, padx=5, pady=5)
            index_row += 1
            headers = ["Mã dịch vụ", "Tên dịch vụ", "Giá"]
            for j, header in enumerate(headers):
                header_label = ctk.CTkLabel(self, text=header, width=70,
                                            height=25)
                header_label.grid(row=index_row, column=j, padx=5, pady=5)

            for j, service in enumerate(s.list_service, start=0):
                data = [service.service_id, service.service_name, service.price]
                index_row += 1
                for k, value in enumerate(data):
                    cell_label = ctk.CTkLabel(self, text=value, width=70,
                                              height=25)
                    cell_label.grid(row=index_row, column=k, padx=5, pady=5)
            index_row += 1
