from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from NumberToText import number_to_text_pl


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
        if type(total) is int:
            return number_to_text_pl(total) + " złotych."
        if type(total) is float:
            if round(total % 1, 2) > 0:
                return number_to_text_pl(int(total)) + " złotych " + number_to_text_pl(round(total % 1, 2)*100) + " groszy."
            else:
                return number_to_text_pl(total) + " złotych."

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