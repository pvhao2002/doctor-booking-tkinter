from dto.service import Service


class InvoiceDetail:
    def __init__(self, model):
        self.invoice_id = model[0]['invoice_id'] if 'invoice_id' in model[0] else ''
        self.total_amount = model[0]['total_amount'] if 'total_amount' in model[0] else ''
        self.create_date = model[0]['create_date'] if 'create_date' in model[0] else ''
        self.payment_status = model[0]['payment_status'] if 'payment_status' in model[0] else ''
        self.status = model[0]['status'] if 'status' in model[0] else ''

        self.list_service = [Service(service) for service in model]
