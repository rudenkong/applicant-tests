import abc

class OrderItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class Order:
    def __init__(self):
        self.items = []
        self.status = 'open'

    def add_item(self, order_item):
        self.items.append(order_item)

    def total_price(self):
        total = 0
        for item in self.items:
            total += item.quantity * item.price
        return total

    def pay(self, payment_processor, security_code):
        payment_processor.process_payment(security_code)
        self.status = 'paid'

class PaymentProcessor:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def process_payment(self, payment_type, security_code):
        pass

class DebitPaymentProcessor:
    def process_payment(self, security_code):
        print('Что-то важное происходит с debit')
        print(f'Верифицируем код: {security_code}')

class CreditPaymentProcessor:
    def process_payment(self, security_code):
        print('credit')
        print(f'Верифицируем код: {security_code}')

def main() -> None:
    order = Order()
    order_item1 = OrderItem('Keyboard', 1, 50)
    order_item2 = OrderItem('SSD', 1, 150)
    order_item3 = OrderItem('USB cable', 2, 5)
    order.add_item(order_item1)
    order.add_item(order_item2)
    order.add_item(order_item3)
    print(order.total_price())

    debit_payment_processor = DebitPaymentProcessor()
    order.pay(debit_payment_processor, '0372846')

if __name__ == "__main__":
    main()