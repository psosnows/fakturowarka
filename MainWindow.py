from PySide2.QtCore import (Slot)
from PySide2.QtWidgets import (QMainWindow, QAction,
                               QApplication)

# get the class that manages all the data


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

        widget.make_load_state(["./domyślne.fkt"])

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()
