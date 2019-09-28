import sys
from PySide2.QtWidgets import QApplication
from filer import Filer

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Filer()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())