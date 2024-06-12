import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt6 import uic
from googletrans import Translator, LANGUAGES

class MW(QMainWindow):
    def __init__(self):
        super(MW, self).__init__()

        # Load the .ui file
        uic.loadUi("translator.ui", self)
        self.setWindowTitle("Translator APP")

        # Widgets
        self.t_button = self.findChild(QPushButton, "pushButton")
        self.c_button = self.findChild(QPushButton, "pushButton_2")

        self.combo_1 = self.findChild(QComboBox, "comboBox")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")

        self.txt_1 = self.findChild(QTextEdit, "textEdit")
        self.txt_2 = self.findChild(QTextEdit, "textEdit_2")

        self.t_button.clicked.connect(self.translate)
        self.c_button.clicked.connect(self.clear)

        # Add languages to the combo boxes
        self.languages = LANGUAGES

        # Convert to list
        self.language_list = list(self.languages.values())

        # Add items to combo boxes
        self.combo_1.addItems(self.language_list)
        self.combo_2.addItems(self.language_list) 

        # Set default combo item 
        self.combo_1.setCurrentText("english")
        self.combo_2.setCurrentText("german")

    def clear(self):
        # Clear the textboxes
        self.txt_1.setText("")
        self.txt_2.setText("")
        
        self.combo_1.setCurrentText("english")
        self.combo_2.setCurrentText("german")

    def translate(self):
        try:
            translator = Translator()

            # Get original language Key
            from_language_key = [key for key, value in self.languages.items() if value == self.combo_1.currentText()][0]
            # Get translated language Key
            to_language_key = [key for key, value in self.languages.items() if value == self.combo_2.currentText()][0]

            # Translate text
            words = self.txt_1.toPlainText()
            translated_text = translator.translate(words, src=from_language_key, dest=to_language_key).text
            self.txt_2.setText(translated_text)
           
        except Exception as e:
            QMessageBox.about(self, "Translator", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
