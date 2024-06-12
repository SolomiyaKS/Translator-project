import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTextEdit, QMEssageBox
from PyQt6 import uic
import googletrans
import textblob

class MW(QMainWindow):
    def __init__(self):
        super(MW, self).__init__()

        #Load the .ui file 
        uic.loadUI("translate.ui", self)
        self.setWindowTitle("Translator APP")

        #Widgets

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
