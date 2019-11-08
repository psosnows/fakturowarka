from PySide2.QtCore import (Slot, QDate, Qt)
from PySide2.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QAction,
                               QApplication, QWidget, QFormLayout, QDateEdit, QLabel,
                               QTableWidget, QHeaderView, QTableWidgetItem, QCheckBox)

# get the class that manages all the data
from input_doc import InputDoc, Item


class DelButton(QPushButton):
    def __init__(self, text, row_number, total=0):
        QPushButton.__init__(self, text)
        self.row = row_number
        self.total = total

    def button_out(self):
        print(self.row)


class TableWidget(QTableWidget):
    def __init__(self, init_items=[]):
        QTableWidget.__init__(self)

        # interaction with Widget that stores the total amount
        # reference to function that resets total amount
        self.reset_total_widget = self.placeholder_function

        # initiate the table
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Nazwa towaru lub usługi", "Jm.", "Ilość", "Cena", "Wartość", ""])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # here we store all the "remove" buttons
        self.buttons = []

        # if there are are initial items provided, add them to the list
        self.replace_items(init_items)

    # adding extra functions that will reduce values in other objects (namely Total Widget)
    def placeholder_function(self):
        pass

    def set_reset_total_widget(self, rst_tot_widg):
        self.reset_total_widget = rst_tot_widg

    def columnAt(self, index):
        col = []
        for i in range(self.rowCount()):
            col.append(self.item(i, index))
        return col

    # wrapper method to add an item
    def add_item(self, item):
        self.add_row(item.name, item.unit, item.amount, item.price)

    # adding a row with values
    def add_row(self, name, unit, quantity, price):

        new_row_num = self.rowCount()

        # create items and widgets
        qw_name = QTableWidgetItem(name)
        qw_unit = QTableWidgetItem(unit)
        qw_quantity = QTableWidgetItem(str(quantity))
        qw_price = QTableWidgetItem(str(price))
        qw_total = QTableWidgetItem(str(float(quantity) * float(price)))
        button = DelButton("Usuń", new_row_num, quantity * price)

        # attach a virtual delete function that takes as the parameter the row of the pressed button
        button.clicked.connect(lambda: self.delete_row(button.row))

        # insert items and widgets to their places
        self.buttons.append(button)
        self.insertRow(new_row_num)
        self.setItem(new_row_num, 0, qw_name)
        self.setItem(new_row_num, 1, qw_unit)
        self.setItem(new_row_num, 2, qw_quantity)
        self.setItem(new_row_num, 3, qw_price)
        self.setItem(new_row_num, 4, qw_total)
        self.setCellWidget(new_row_num, 5, self.buttons[new_row_num])

        # connect to event when any cell is changed
        self.cellChanged.connect(self.recalc_total)

    # test function to remove first row
    def del_first_row(self):
        self.delete_row(0)

    # delete a particular row in the table
    def delete_row(self, index):
        self.removeRow(index)

        # self.reduce_totals(self.buttons[index].total)
        self.reset_total_widget(self.get_total())

        # each del button has an attached row index to it
        # we need to update these row indexes since we removed an row
        for i in range(index, len(self.buttons)):
            self.buttons[i].row -= 1
        self.buttons.pop(index)

    def get_total(self) -> float:
        total = 0.0
        if self.rowCount() > 0:
            for am, pr in zip(self.columnAt(2), self.columnAt(3)):
                total += float(am.text()) * float(pr.text())

        return total

    def get_items(self):
        items = []
        for nam, uni, am, pr in zip(self.columnAt(0),self.columnAt(1),self.columnAt(2),self.columnAt(3)):
            items.append(Item(nam.text(), uni.text(), am.text(), pr.text()))
        return items

    def recalc_total(self):
        items = self.selectedItems()
        if items:
            nth_row = items[0].row()
            new_total = float(self.item(nth_row, 2).text()) * float(self.item(nth_row, 3).text())
            self.item(nth_row, 4).setText("%.2f" % new_total)
            self.reset_total_widget(self.get_total())

    def replace_items(self, new_items=[]):
        while self.rowCount() > 0:
            self.del_first_row()
        for item in new_items:
            self.add_item(item)



class TotalWidget(QWidget):
    def __init__(self, tot_widget, box, init_total=0):
        QWidget.__init__(self)
        self.total_worded_widget = tot_widget
        self.checkbox = box
        self.total = init_total
        self.total_label = QLabel("Razem:\t%.2f zł" % self.total)
        self.total_worded_widget.setAlignment(Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.total_label, alignment=Qt.AlignRight)
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.checkbox)
        text_layout.addWidget(self.total_worded_widget)
        main_layout.addLayout(text_layout)

        self.setLayout(main_layout)

    def number_to_pl_words(self, total):
        """
        TODO : we need to add the functions
        """
        return str("%.2f złotych" % total)

    def increase_total(self, amount):
        self.total += amount
        self.reset_text()

    def decrease_total(self, amount):
        self.total -= amount
        self.reset_text()

    def reset_total(self, value):
        self.total = value
        self.reset_text()

    def reset_text(self):
        self.total_label.setText("Razem:\t%.2f zł" % self.total)
        if self.checkbox.isChecked():
            new_text = self.number_to_pl_words(self.total)
            self.total_worded_widget.setText(new_text)


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

        self.input_item_name = QLineEdit("<Wprowadź nazwę towaru>")
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
        # it will pass its "reduce_total" function to Table Widget so we can sew it into Del buttons
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
        layout = QVBoxLayout()
        layout.addWidget(self.widget_place_dates, alignment=Qt.AlignRight)
        layout.addWidget(self.widget_seller_buyer)

        layout.addWidget(self.widget_doc_id)

        layout.addWidget(self.widget_new_item)
        layout.addWidget(self.table)
        layout.addWidget(self.total)

        layout.addWidget(self.widget_payment)

        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.generate_pdf)

    def add_item(self):
        new_item = Item(self.input_item_name.text(),
                        self.input_item_unit.text(),
                        int(self.input_item_quantity.text()),
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
            self.input_auto_generate
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
                           item.amount + " & " + \
                           "%.2f" % float(item.price) + " & " + \
                           "%.2f" % (float(item.amount)*float(item.price)) + " \\\\ \n"
            items_input += "\t\t\hline\n"

        env = make_env(loader=FileSystemLoader('.'))
        tpl = env.get_template('latex_template.tex')
        rnd = tpl.render(
            place=f.place.__str__(),
            make_date=f.make_date.__str__(),
            sell_date=f.sell_date.__str__(),
            sellers_name=f.sellers_name.__str__(),
            sellers_id=f.sellers_id.__str__(),
            sellers_address=f.sellers_address.__str__(),
            sellers_post=f.sellers_post.__str__(),
            sellers_city=f.sellers_city.__str__(),
            buyers_name=f.buyers_name.__str__(),
            buyers_id=f.buyers_id.__str__(),
            buyers_address=f.buyers_address.__str__(),
            buyers_post=f.buyers_post.__str__(),
            buyers_city=f.buyers_city.__str__(),
            bills_id=f.bills_id.__str__(),
            worded_total_payment=f.worded_total_payment.__str__(),
            payment_method=f.payment_method.__str__(),
            payment_due_date=f.payment_due_date.__str__(),
            payment_account=f.payment_account.__str__(),
            total="%.2f" % self.total.total,
            # items=str("")
            items=str(items_input)
        )
        pdf = build_pdf(rnd,builder="pdflatex")
        save_to_location = QFileDialog.getSaveFileName(self, "Zapisz wygenerowany dokument", ".", "Plik PDF (*.pdf *.PDF)")
        if save_to_location[0]:
            pdf.save_to(save_to_location[0])
            self.status.showMessage("Wygenerowano i zapisano PDF", 2000)
        else:
            self.status.showMessage("NIE zapisano pliku PDF", 2000)

    def save_state(self):
        from PySide2.QtWidgets import QFileDialog
        app_data = self.generate_data()
        save_to_location = QFileDialog.getSaveFileName(self, "Zapisz pracę", ".", "Plik fkt (*.fkt)")
        if save_to_location[0]:
            with open(save_to_location[0], 'w') as file:
                file.write(str(app_data))
        self.status.showMessage("Zapisano pracę", 2000)
        self.block_all(2000)

    def load_state(self):
        from PySide2.QtWidgets import QFileDialog
        from input_doc import Item, InputDoc
        file_location = QFileDialog.getOpenFileName(self, "Wczytaj pracę", ".", "Plik fkt (*.fkt)")
        if file_location[0]:
            with open(file_location[0], 'r') as file:
                read_data = []
                for line in file:
                    read_data.append(line.replace('\n',''))
                item_cnt = int(read_data[22])
                items = []
                if item_cnt > 0:
                    for i in range(0, item_cnt):
                        items.append(Item(read_data[i*4+23], read_data[i*4+24], read_data[i*4+25], read_data[i*4+26]))
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
                    init_item_input_quantity=read_data[20],
                    init_item_input_price=read_data[21]
                )
                self.set_state(loaded_state)
                self.status.showMessage("Wczytano pracę", 2000)

    def toggle_text_generator(self):
        if self.input_auto_generate.isChecked():
            self.input_worded_total_payment.setDisabled(True)
            self.total.reset_text()
        else:
            self.input_worded_total_payment.setDisabled(False)

    def set_state(self, doc_data):
        self.input_place.setText(doc_data.place),
        date = doc_data.make_date.split('.')
        self.input_make_date.setDate(QDate(int(date[0]), int(date[1]), int(date[2]))),
        date = doc_data.sell_date.split('.')
        self.input_sell_date.setDate(QDate(int(date[0]), int(date[1]), int(date[2]))),
        self.input_sellers_name.setText(doc_data.sellers_name),
        self.input_sellers_id.setText(doc_data.sellers_id),
        self.input_sellers_address.setText(doc_data.sellers_address),
        self.input_sellers_post.setText(doc_data.sellers_post),
        self.input_sellers_city.setText(doc_data.sellers_city),
        self.input_buyers_name.setText(doc_data.buyers_name),
        self.input_buyers_id.setText(doc_data.buyers_id),
        self.input_buyers_address.setText(doc_data.buyers_address),
        self.input_buyers_post.setText(doc_data.buyers_post),
        self.input_buyers_city.setText(doc_data.buyers_city),
        self.input_bills_id.setText(doc_data.bills_id),
        self.input_worded_total_payment.setText(doc_data.worded_total_payment),
        self.input_payment_method.setText(doc_data.payment_method),
        date = doc_data.payment_due_date.split('.')
        self.input_payment_due_date.setDate(QDate(int(date[0]), int(date[1]), int(date[2]))),
        self.input_payment_account.setText(doc_data.payment_account),
        self.input_item_name.setText(doc_data.item_input_name),
        self.input_item_unit.setText(doc_data.item_input_unit),
        self.input_item_quantity.setText(doc_data.item_input_quantity),
        self.input_item_price.setText(doc_data.item_input_price),
        self.input_auto_generate.setDisabled(doc_data.auto_generate)
        self.toggle_text_generator()
        self.table.replace_items(doc_data.items)

    def connect_status(self, st):
        self.status = st


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Fakturowarka")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Plik")

        # Load state QAction
        load_state_action = QAction("Otwórz pracę", self)
        load_state_action.setShortcut("Ctrl+L")
        load_state_action.triggered.connect(widget.load_state)

        self.file_menu.addAction(load_state_action)

        # Save state QAction
        save_state_action = QAction("Zapisz pracę", self)
        save_state_action.setShortcut("Ctrl+S")
        save_state_action.triggered.connect(widget.save_state)

        self.file_menu.addAction(save_state_action)

        # Exit QAction
        exit_action = QAction("Zakończ", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        self.setCentralWidget(widget)

        self.status = self.statusBar()
        widget.connect_status(self.status)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()
