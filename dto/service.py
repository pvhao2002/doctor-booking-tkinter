class Service:
    def __init__(self, model):
        self.service_id = model['service_id'] if 'service_id' in model else ''
        self.service_name = model['service_name'] if 'service_name' in model else ''
        self.description = model['description'] if 'description' in model else ''
        self.price = model['price'] if 'price' in model else ''
        self.status = model['status'] if 'status' in model else ''

    def __str__(self):
        return f'{self.service_id} - {self.service_name} - {self.description} - {self.price} - {self.status}'
