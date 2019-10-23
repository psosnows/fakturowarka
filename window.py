# get the sweet pyside QT widgets
from PySide2.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QAction,
                               QApplication, QWidget, QFormLayout, QDateEdit, QLabel,
                               QTableWidget, QHeaderView, QTableWidgetItem)
from PySide2.QtCore import (Slot, QDate, Qt)

# get the class that manages all the data
from input_doc import InputDoc


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
        self.input_items = QLineEdit("Miejsce na to co sprzedajemy")
        self.input_worded_total_payment = QLineEdit(self.data.worded_total_payment)
        self.input_payment_method = QLineEdit(self.data.payment_method)
        self.input_payment_due_date = QDateEdit()
        self.input_payment_due_date.setDate(QDate.currentDate())
        self.input_payment_account = QLineEdit(self.data.payment_account)

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
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nazwa towaru lub usługi", "Jm.", "Ilość", "Cena", "Wartość", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.insertRow(0)
        self.someinput = QTableWidgetItem("some text")
        self.someinput2 = QTableWidgetItem("some text")
        self.delButton = QPushButton("Usuń")

        self.table.setItem(0,0,self.someinput)
        self.table.setItem(0,1,self.someinput2)
        self.table.setCellWidget(0,5,self.delButton)


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

        # TODO: table inputs
        layout.addWidget(self.table)
        layout.addWidget(self.input_worded_total_payment)

        layout.addWidget(self.widget_payment)

        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())


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
