from PySide2.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from DelButton import DelButton
from input_doc import Item


class TableWidget(QTableWidget):
    def __init__(self, init_items=[]):
        QTableWidget.__init__(self)

        # interaction with Widget that stores the total amount
        # reference to function that resets total amount
        self.reset_total_widget = self.placeholder_function

        # initiate the table
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Towar lub usługa", "Jm.", "Ilość", "Cena", "Wartość", ""])
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
        qw_quantity = QTableWidgetItem(quantity)
        qw_price = QTableWidgetItem(price)
        qw_total = QTableWidgetItem(str(float(quantity) * float(price)))
        button = DelButton("Usuń", new_row_num, float(quantity) * float(price))

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
        rc = self.rowCount()
        if rc > 0:
            for am, pr in zip(self.columnAt(2), self.columnAt(3)):
                total += float(am.text()) * float(pr.text())

        return total

    def get_items(self):
        items = []
        for nam, uni, am, pr in zip(self.columnAt(0), self.columnAt(1), self.columnAt(2), self.columnAt(3)):
            items.append(Item(nam.text(), uni.text(), am.text(), pr.text()))
        return items

    def recalc_total(self, row, col):
        items = self.selectedItems()
        if items and items[0].column() == col and items[0].row() == row:
            nth_row = items[0].row()
            new_total = float(self.item(nth_row, 2).text()) * float(self.item(nth_row, 3).text())
            self.item(nth_row, 4).setText("%.2f" % new_total)
            self.reset_total_widget(self.get_total())

    def replace_items(self, new_items=[]):
        while self.rowCount() > 0:
            self.del_first_row()
        for item in new_items:
            self.add_item(item)
