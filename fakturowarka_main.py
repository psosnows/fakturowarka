import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class InputDoc:
    class Item:
        def __init__(self, init_name='nazwa towaru', init_unit='j.m.', init_amount=1, init_price=0.0):
            self.name = init_name
            self.unit = init_unit
            self.amount = init_amount
            self.price = init_price

    def __init__(self,
                 init_place='<miejce>',
                 init_make_date='dd-mm-yyyy',
                 init_sell_date='dd-mm-yyyy',
                 init_sellers_name='Grażyna Sosnowska',
                 init_sellers_id='PESEL: 01010112345',
                 init_sellers_address='Spokojna 7',
                 init_sellers_post='80-297',
                 init_sellers_city='Baninio',
                 init_buyers_name='<nazwa firmy>',
                 init_buyers_id='NIP: <01010112345>',
                 init_buyers_address='<ulica>',
                 init_buyers_post='<kod pocztowy>',
                 init_buyers_city='<miejscowość>',
                 init_bills_id='0',
                 init_items=[Item()],
                 init_worded_total_payment='zero złotych',
                 init_payment_menthod='przelew',
                 init_payment_due_date='dd-mm-yyyy',
                 init_payment_account='12 1234 1234 1234 1234 1234'
                 ):
        self.place = init_place
        self.make_date = init_make_date
        self.sell_date = init_sell_date
        self.sellers_name = init_sellers_name
        self.sellers_ID = init_sellers_id
        self.sellers_address = init_sellers_address
        self.sellers_post = init_sellers_post
        self.sellers_city = init_sellers_city
        self.buyers_name = init_buyers_name
        self.buyers_id = init_buyers_id
        self.buyers_address = init_buyers_address
        self.buyers_post = init_buyers_post
        self.buyers_city = init_buyers_city
        self.bills_id = init_bills_id
        self.items = init_items
        self.worded_total_payment = init_worded_total_payment
        self.payment_method = init_payment_menthod
        self.payment_due_date = init_payment_due_date
        self.payment_account = init_payment_account


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.edit.selectAll()
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())