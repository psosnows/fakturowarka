from PySide2.QtCore import QDate, Qt
from PySide2.QtWidgets import QWidget, QLineEdit, QDateEdit, QCheckBox, QFormLayout, QLabel, QHBoxLayout, QPushButton, \
    QGridLayout, QVBoxLayout

from TableWidget import TableWidget
from TotalWidget import TotalWidget
from input_doc import Item, InputDoc


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.status = ""

        # Create inputs
        self.input_place = QLineEdit('Gdańsk')
        self.input_make_date = QDateEdit()
        self.input_make_date.setDate(QDate.currentDate())
        self.input_sell_date = QDateEdit()
        self.input_sell_date.setDate(QDate.currentDate())
        self.input_sellers_name = QLineEdit('Grażyna Sosnowska')
        self.input_sellers_id = QLineEdit('PESEL: 01010112345')
        self.input_sellers_address = QLineEdit('Spokojna 7')
        self.input_sellers_post = QLineEdit('80-297')
        self.input_sellers_city = QLineEdit('Banino')
        self.input_buyers_name = QLineEdit('<nazwa firmy>')
        self.input_buyers_id = QLineEdit('NIP: 123')
        self.input_buyers_address = QLineEdit('<ulica i numer domu>')
        self.input_buyers_post = QLineEdit('00-000')
        self.input_buyers_city = QLineEdit('<miasto>')
        self.input_bills_id = QLineEdit('R/01/'+str(QDate.currentDate().month())+'/'+str(QDate.currentDate().year()))
        self.input_auto_generate = QCheckBox("Generuj automatycznie")
        self.input_auto_generate.setChecked(True)
        self.input_auto_generate.clicked.connect(self.toggle_text_generator)
        self.input_worded_total_payment = QLineEdit('zero złotych')
        self.input_worded_total_payment.setDisabled(True)
        self.input_payment_method = QLineEdit('przelew')
        self.input_payment_due_date = QDateEdit()
        self.input_payment_due_date.setDate(QDate.currentDate())
        self.input_payment_account = QLineEdit('<IBAN konta do przelewu>')

        self.input_item_name = QLineEdit("<Podaj nazwę towaru>")
        self.input_item_unit = QLineEdit("osobo-doba")
        self.input_item_quantity = QLineEdit("1")
        self.input_item_price = QLineEdit("25")

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
        self.item_add_button.clicked.connect(self.add_item)
        self.layout_item_input = QGridLayout()
        self.layout_item_input.addWidget(QLabel("Nazwa towaru"), 0, 0)
        self.layout_item_input.addWidget(QLabel("Jm."), 0, 1)
        self.layout_item_input.addWidget(QLabel("Ilość"), 0, 2)
        self.layout_item_input.addWidget(QLabel("Cena jednostki"), 0, 3)
        self.layout_item_input.addWidget(QLabel(""), 0, 4)
        self.layout_item_input.addWidget(self.input_item_name, 1, 0)
        self.layout_item_input.addWidget(self.input_item_unit, 1, 1)
        self.layout_item_input.addWidget(self.input_item_quantity, 1, 2)
        self.layout_item_input.addWidget(self.input_item_price, 1, 3)
        self.layout_item_input.addWidget(self.item_add_button, 1, 4)
        self.widget_new_item = QWidget()
        self.widget_new_item.setLayout(self.layout_item_input)

        # first we create a widget that contains the totals
        # it will pass its "reset total" function to Table Widget so we can sew it into Del buttons
        self.total = TotalWidget(self.input_worded_total_payment, self.input_auto_generate)

        self.table = TableWidget()
        self.table.set_reset_total_widget(self.total.reset_total)

        # payment details
        self.layout_payment = QFormLayout()
        self.layout_payment.addRow("Sposób płatności", self.input_payment_method)
        self.layout_payment.addRow("Termin płatności", self.input_payment_due_date)
        self.layout_payment.addRow("Numer rachunku", self.input_payment_account)
        self.widget_payment = QWidget()
        self.widget_payment.setFixedWidth(300)
        self.widget_payment.setLayout(self.layout_payment)

        # end button
        self.button = QPushButton("Generuj PDF")

        # Create layout and add widgets

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.widget_payment)
        top_layout.addWidget(self.widget_place_dates, alignment=Qt.AlignRight)

        layout = QVBoxLayout()

        layout.addLayout(top_layout)

        layout.addWidget(self.widget_seller_buyer)

        layout.addWidget(self.widget_doc_id)

        layout.addWidget(self.widget_new_item)
        layout.addWidget(self.table)
        layout.addWidget(self.total)

        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.generate_pdf)

    def add_item(self):
        new_item = Item(self.input_item_name.text(),
                        self.input_item_unit.text(),
                        float(self.input_item_quantity.text()),
                        float(self.input_item_price.text()))
#        self.data.items.append(new_item)
        self.table.add_item(new_item)
        self.total.increase_total(new_item.amount * new_item.price)

    def generate_data(self):
        items = self.table.get_items()
        return InputDoc(
            self.input_place.text(),
            self.input_make_date.text(),
            self.input_sell_date.text(),
            self.input_sellers_name.text(),
            self.input_sellers_id.text(),
            self.input_sellers_address.text(),
            self.input_sellers_post.text(),
            self.input_sellers_city.text(),
            self.input_buyers_name.text(),
            self.input_buyers_id.text(),
            self.input_buyers_address.text(),
            self.input_buyers_post.text(),
            self.input_buyers_city.text(),
            self.input_bills_id.text(),
            items,
            self.input_worded_total_payment.text(),
            self.input_payment_method.text(),
            self.input_payment_due_date.text(),
            self.input_payment_account.text(),
            self.input_item_name.text(),
            self.input_item_unit.text(),
            self.input_item_quantity.text(),
            self.input_item_price.text(),
            self.input_auto_generate.isChecked()
        )

    def generate_pdf(self):
        from jinja2.loaders import FileSystemLoader
        from latex.jinja2 import make_env
        from latex import build_pdf
        from PySide2.QtWidgets import QFileDialog

        f = self.generate_data()

        items_input = ""
        for i, item in enumerate(f.items):
            items_input += "\t\t%d & " % (i+1) + \
                           str(item.name) + " & " + \
                           str(item.unit) + " & " + \
                           str(item.amount) + " & " + \
                           "%.2f" % float(item.price) + " & " + \
                           "%.2f" % (float(item.amount)*float(item.price)) + " \\\\ \n"
            items_input += "\t\t\hline\n"

        env = make_env(loader=FileSystemLoader('.'))
        tpl = env.get_template('latex_template.tex')
        rnd = tpl.render(
            place=str(f.place),
            make_date=str(f.make_date),
            sell_date=str(f.sell_date),
            sellers_name=str(f.sellers_name),
            sellers_id=str(f.sellers_id),
            sellers_address=str(f.sellers_address),
            sellers_post=str(f.sellers_post),
            sellers_city=str(f.sellers_city),
            buyers_name=str(f.buyers_name),
            buyers_id=str(f.buyers_id),
            buyers_address=str(f.buyers_address),
            buyers_post=str(f.buyers_post),
            buyers_city=str(f.buyers_city),
            bills_id=str(f.bills_id),
            worded_total_payment=str(f.worded_total_payment),
            payment_method=str(f.payment_method),
            payment_due_date=str(f.payment_due_date),
            payment_account=str(f.payment_account),
            total="%.2f" % self.total.total,
            items=str(items_input)
        )
        pdf = build_pdf(rnd, builder="pdflatex")
        save_to_location = QFileDialog.getSaveFileName(self, "Zapisz wygenerowany dokument", ".", "Plik PDF (*.pdf *.PDF)")
        if save_to_location[0]:
            try:
                pdf.save_to(save_to_location[0])
                self.status.showMessage("Wygenerowano i zapisano PDF", 5000)
            except PermissionError:
                self.status.showMessage("Błąd! Nie można zapisać do tego pliku, brak dostępu.", 5000)
        else:
            self.status.showMessage("NIE zapisano pliku PDF", 5000)

    def save_state(self):
        from PySide2.QtWidgets import QFileDialog
        app_data = self.generate_data()
        save_to_location = QFileDialog.getSaveFileName(self, "Zapisz pracę", ".", "Plik fkt (*.fkt)")
        if save_to_location[0]:
            with open(save_to_location[0], 'w') as file:
                file.write(str(app_data))
        self.status.showMessage("Zapisano pracę", 5000)

    def load_state(self):
        from PySide2.QtWidgets import QFileDialog
        file_location = QFileDialog.getOpenFileName(self, "Wczytaj pracę", ".", "Plik fkt (*.fkt)")
        self.make_load_state(file_location)

    def make_load_state(self, file_location):
        if file_location[0]:
            try:
                with open(file_location[0], 'r') as file:
                    read_data = []
                    for line in file:
                        read_data.append(line.replace('\n', ''))
                    item_cnt = int(read_data[23])
                    items = []
                    if item_cnt > 0:
                        for i in range(0, item_cnt):
                            items.append(Item(read_data[i*4+24], read_data[i*4+25], read_data[i*4+26], read_data[i*4+27]))
                    box_state = False if read_data[22] == 'False' else True
                    loaded_state = InputDoc(
                        init_place=read_data[0],
                        init_make_date=read_data[1],
                        init_sell_date=read_data[2],
                        init_sellers_name=read_data[3],
                        init_sellers_id=read_data[4],
                        init_sellers_address=read_data[5],
                        init_sellers_post=read_data[6],
                        init_sellers_city=read_data[7],
                        init_buyers_name=read_data[8],
                        init_buyers_id=read_data[9],
                        init_buyers_address=read_data[10],
                        init_buyers_post=read_data[11],
                        init_buyers_city=read_data[12],
                        init_bills_id=read_data[13],
                        init_items=items,
                        init_worded_total_payment=read_data[14],
                        init_payment_menthod=read_data[15],
                        init_payment_due_date=read_data[16],
                        init_payment_account=read_data[17],
                        init_item_input_name=read_data[18],
                        init_item_input_unit=read_data[19],
                        init_item_input_quantity=float(read_data[20]),
                        init_item_input_price=float(read_data[21]),
                        init_auto_generate=box_state
                    )
                    self.set_state(loaded_state)
                    self.status.showMessage("Wczytano pracę", 2000)
            except FileNotFoundError:
                self.status.showMessage("Wczytano stan zero. Brak pliku startowego: domyślne.fkt", 2000)

    def toggle_text_generator(self):
        if self.input_auto_generate.isChecked():
            self.input_worded_total_payment.setDisabled(True)
            self.total.reset_text()
        else:
            self.input_worded_total_payment.setDisabled(False)

    def set_state(self, doc_data):
        self.input_place.setText(doc_data.place)
        date = doc_data.make_date.split('.')
        self.input_make_date.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))
        date = doc_data.sell_date.split('.')
        self.input_sell_date.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))
        self.input_sellers_name.setText(doc_data.sellers_name)
        self.input_sellers_id.setText(doc_data.sellers_id)
        self.input_sellers_address.setText(doc_data.sellers_address)
        self.input_sellers_post.setText(doc_data.sellers_post)
        self.input_sellers_city.setText(doc_data.sellers_city)
        self.input_buyers_name.setText(doc_data.buyers_name)
        self.input_buyers_id.setText(doc_data.buyers_id)
        self.input_buyers_address.setText(doc_data.buyers_address)
        self.input_buyers_post.setText(doc_data.buyers_post)
        self.input_buyers_city.setText(doc_data.buyers_city)
        self.input_bills_id.setText(doc_data.bills_id)
        self.input_worded_total_payment.setText(doc_data.worded_total_payment)
        self.input_payment_method.setText(doc_data.payment_method)
        date = doc_data.payment_due_date.split('.')
        self.input_payment_due_date.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))
        self.input_payment_account.setText(doc_data.payment_account)
        self.input_item_name.setText(doc_data.item_input_name)
        self.input_item_unit.setText(doc_data.item_input_unit)
        self.input_item_quantity.setText(str(doc_data.item_input_quantity))
        self.input_item_price.setText(str(doc_data.item_input_price))
        self.input_auto_generate.setChecked(bool(doc_data.auto_generate))
        self.toggle_text_generator()
        self.table.replace_items(doc_data.items)
        self.total.reset_total(self.table.get_total())

    def connect_status(self, st):
        self.status = st
