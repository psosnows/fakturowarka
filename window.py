from PySide2.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QAction,
                               QApplication, QWidget, QFormLayout, QDateEdit, QLabel,
                               QTableWidget, QHeaderView, QTableWidgetItem)
from PySide2.QtCore import (Slot, QDate, Qt)

# get the class that manages all the data
from input_doc import InputDoc, Item


class DelButton(QPushButton):
    def __init__(self, text, row_number):
        QPushButton.__init__(self, text)
        self.row = row_number
    def buttonOut(self):
        print(self.row)

class TableWidget(QTableWidget):
    def __init__(self, init_items):
        QTableWidget.__init__(self)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Nazwa towaru lub usługi", "Jm.", "Ilość", "Cena", "Wartość", ""])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rows = 0
        self.buttons = []

        if init_items:
            for it in init_items:
                self.addItem(it)

    def addItem(self, item):
        self.addRow(item.name, item.unit, item.amount, item.price)

    def addRow(self, name, unit, quantity, price):
        qw_name = QTableWidgetItem(name)
        qw_unit = QTableWidgetItem(unit)
        qw_quantity = QTableWidgetItem(str(quantity))
        qw_price = QTableWidgetItem(str(price))
        qw_total = QTableWidgetItem(str(float(quantity) * float(price)))
        button = DelButton("Usuń", self.rows)

        # attach a virtual delete function that takes as the parameter the row of the pressed button
        button.clicked.connect(lambda: self.deleteRow(button.row))

        self.buttons.append(button)
        self.insertRow(self.rows)
        self.setItem(self.rows, 0, qw_name)
        self.setItem(self.rows, 1, qw_unit)
        self.setItem(self.rows, 2, qw_quantity)
        self.setItem(self.rows, 3, qw_price)
        self.setItem(self.rows, 4, qw_total)
        self.setCellWidget(self.rows, 5, self.buttons[self.rows])
        self.rows += 1

    def delFirstRow(self):
        self.deleteRow(0)

    def deleteRow(self,index):
        self.removeRow(index)
        for i in range(index, len(self.buttons)):
            self.buttons[i].row -= 1
        self.buttons.pop(index)
        self.rows -= 1


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Initialize data
        self.data = InputDoc()

        # Create inputs
        self.input_place = QLineEdit(self.data.place)
        self.input_make_date = QDateEdit()
        self.input_make_date.setDate(QDate.currentDate())
        self.input_sell_date = QDateEdit()
        self.input_sell_date.setDate(QDate.currentDate())
        self.input_sellers_name = QLineEdit(self.data.sellers_name)
        self.input_sellers_id = QLineEdit(self.data.sellers_id)
        self.input_sellers_address = QLineEdit(self.data.sellers_address)
        self.input_sellers_post = QLineEdit(self.data.sellers_post)
        self.input_sellers_city = QLineEdit(self.data.sellers_city)
        self.input_buyers_name = QLineEdit(self.data.buyers_name)
        self.input_buyers_id = QLineEdit(self.data.buyers_id)
        self.input_buyers_address = QLineEdit(self.data.buyers_address)
        self.input_buyers_post = QLineEdit(self.data.buyers_post)
        self.input_buyers_city = QLineEdit(self.data.buyers_city)
        self.input_bills_id = QLineEdit(self.data.bills_id)
        self.input_worded_total_payment = QLineEdit(self.data.worded_total_payment)
        self.input_payment_method = QLineEdit(self.data.payment_method)
        self.input_payment_due_date = QDateEdit()
        self.input_payment_due_date.setDate(QDate.currentDate())
        self.input_payment_account = QLineEdit(self.data.payment_account)

        self.input_item_name = QLineEdit("<Wprowadź nazwę towaru>")
        self.input_item_unit = QLineEdit("<jednostka>")
        self.input_item_quantity = QLineEdit("<ilość>")
        self.input_item_price = QLineEdit("<cena jednostki>")


        # Create widgets: top widget
        self.layout_place_dates = QFormLayout()
        self.layout_place_dates.addRow("Miejsce wystawienia", self.input_place)
        self.layout_place_dates.addRow("Data wystawienia", self.input_make_date)
        self.layout_place_dates.addRow("Data Sprzedaży", self.input_sell_date)
        self.widget_place_dates = QWidget()
        self.widget_place_dates.setFixedWidth(300)
        self.widget_place_dates.setLayout(self.layout_place_dates)

        # Create widgets: seller
        self.layout_seller = QFormLayout()
        self.seller_label = QLabel("SPRZEDAWCA")
        self.seller_label.setStyleSheet("{color: #C0BBFE}")
        self.layout_seller.addWidget(self.seller_label)
        
        self.layout_seller.addRow("Dane sprzedawcy", self.input_sellers_name)
        self.layout_seller.addRow("PESEL / NIP", self.input_sellers_id)
        self.layout_seller.addRow("Adres", self.input_sellers_address)
        self.layout_seller.addRow("Kod pocztowy", self.input_sellers_post)
        self.layout_seller.addRow("Miasto", self.input_sellers_city)

        self.widget_seller = QWidget()
        self.widget_seller.setLayout(self.layout_seller)

        # Create widgets: buyer
        self.layout_buyer = QFormLayout()
        self.buyer_label = QLabel("NABYWCA")
        self.buyer_label.setStyleSheet("{color: #C0BBFE}")
        self.layout_buyer.addWidget(self.buyer_label)

        self.layout_buyer.addRow("Dane nabywcy", self.input_buyers_name)
        self.layout_buyer.addRow("PESEL / NIP", self.input_buyers_id)
        self.layout_buyer.addRow("Adres", self.input_buyers_address)
        self.layout_buyer.addRow("Kod pocztowy", self.input_buyers_post)
        self.layout_buyer.addRow("Miasto", self.input_buyers_city)

        self.widget_buyer = QWidget()
        self.widget_buyer.setLayout(self.layout_buyer)

        # combining seller and buyer to one widget
        self.layout_seller_buyer = QHBoxLayout()
        self.layout_seller_buyer.addWidget(self.widget_seller)
        self.layout_seller_buyer.addSpacing(30)
        self.layout_seller_buyer.addWidget(self.widget_buyer)
        self.widget_seller_buyer = QWidget()
        self.widget_seller_buyer.setLayout(self.layout_seller_buyer)

        # bill number
        self.layout_doc_id = QFormLayout()
        self.layout_doc_id.addRow("Numer Rachunku", self.input_bills_id)
        self.widget_doc_id = QWidget()
        self.widget_doc_id.setLayout(self.layout_doc_id)

        # items
        self.item_add_button = QPushButton("Dodaj")
        self.item_add_button.clicked.connect(self.addItem)
        self.layout_item_input = QGridLayout()
        self.layout_item_input.addWidget(QLabel("Nazwa towaru"),0,0)
        self.layout_item_input.addWidget(QLabel("Jm."),0,1)
        self.layout_item_input.addWidget(QLabel("Ilość"),0,2)
        self.layout_item_input.addWidget(QLabel("Cena jednostki"),0,3)
        self.layout_item_input.addWidget(QLabel(""),0,4)
        self.layout_item_input.addWidget(self.input_item_name,1,0)
        self.layout_item_input.addWidget(self.input_item_unit,1,1)
        self.layout_item_input.addWidget(self.input_item_quantity,1,2)
        self.layout_item_input.addWidget(self.input_item_price,1,3)
        self.layout_item_input.addWidget(self.item_add_button,1,4)
        self.widget_new_item = QWidget()
        self.widget_new_item.setLayout(self.layout_item_input)

        self.table = TableWidget(self.data.items)

        # payment details
        self.layout_payment = QFormLayout()
        self.layout_payment.addRow("Sposób płatności", self.input_payment_method)
        self.layout_payment.addRow("Termin płatności", self.input_payment_due_date)
        self.layout_payment.addRow("Numer rachunku", self.input_payment_account)
        self.widget_payment = QWidget()
        self.widget_payment.setFixedWidth(300)
        self.widget_payment.setLayout(self.layout_payment)

        # end button
        self.button = QPushButton("Show Greetings")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.widget_place_dates, alignment=Qt.AlignRight)
        layout.addWidget(self.widget_seller_buyer)

        layout.addWidget(self.widget_doc_id)

        layout.addWidget(self.widget_new_item)
        layout.addWidget(self.table)
        layout.addWidget(self.input_worded_total_payment)

        layout.addWidget(self.widget_payment)

        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    def addItem(self):
        new_item = Item(self.input_item_name.text(),
                        self.input_item_unit.text(),
                        int(self.input_item_quantity.text()),
                        float(self.input_item_price.text()))
        self.data.items.append(new_item)
        self.table.addItem(new_item)

    # Greets the user
    def greetings(self):
        print ("Hello")


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Fakturowarka")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Plik")

        # Exit QAction
        exit_action = QAction("Zakończ", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()
