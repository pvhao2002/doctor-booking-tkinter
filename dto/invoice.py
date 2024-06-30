class Invoice:
    def __init__(self, model):
        self.invoice_id = model['invoice_id'] if 'invoice_id' in model else ''
        self.appointment_id = model['appointment_id'] if 'appointment_id' in model else ''
        self.total_amount = model['total_amount'] if 'total_amount' in model else ''
        self.create_date = model['create_date'] if 'create_date' in model else ''
        self.payment_status = model['payment_status'] if 'payment_status' in model else ''
