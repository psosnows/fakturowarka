import sys

# get the form that works the inputs
from window import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)

    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())