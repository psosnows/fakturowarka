from PySide2.QtWidgets import QPushButton


class DelButton(QPushButton):
    def __init__(self, text, row_number, total=0):
        QPushButton.__init__(self, text)
        self.row = row_number
        self.total = total

    def button_out(self):
        print(self.row)
