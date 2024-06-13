import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTextEdit, QMessageBox, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6 import uic
from googletrans import Translator, LANGUAGES

class MW(QMainWindow):
    def __init__(self):
        super(MW, self).__init__()

        # Load the .ui file
        uic.loadUi("translator.ui", self)
        self.setWindowTitle("Translator APP")

        # Set window icon
        app_icon = QIcon("D:\\Qt_projects\\translator\\icons\\icon.png")
        self.setWindowIcon(app_icon)

        # Widgets
        self.t_button = self.findChild(QPushButton, "translate_btn")
        self.c_button = self.findChild(QPushButton, "clear_btn")
        self.copy_button = self.findChild(QPushButton, "copy_btn")
        self.recent_button = self.findChild(QPushButton, "recent_btn")

        self.combo_1 = self.findChild(QComboBox, "comboBox_1")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")

        self.txt_1 = self.findChild(QTextEdit, "textEdit_1")
        self.txt_2 = self.findChild(QTextEdit, "textEdit_2")

        self.t_button.clicked.connect(self.translate)
        self.c_button.clicked.connect(self.clear)
        self.copy_button.clicked.connect(self.copy_text)
        self.recent_button.clicked.connect(self.show_recent)

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

        # List to store recent translations
        self.recent_translations = []

    # Clear the textboxes
    def clear(self):
        self.txt_1.setText("")
        self.txt_2.setText("")
        
        self.combo_1.setCurrentText("english")
        self.combo_2.setCurrentText("german")

    # Copy translated text to clipboard
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_2.toPlainText())

    # Translate the text
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

            # Save the recent translation
            self.recent_translations.append((words, translated_text))
            if len(self.recent_translations) > 10:  # Limit to last 10 translations
                self.recent_translations.pop(0)

        except Exception as e:
            QMessageBox.about(self, "Translator", str(e))

    # Show recent translations
    def show_recent(self):
        # Show recent translations in a dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle("Recent Translations")
        dialog.setGeometry(450, 200, 400, 200)
        layout = QVBoxLayout()

        # Create QListWidget for displaying translations
        list_widget = QListWidget()

        # Set text style
        font = QFont()
        font.setPointSize(14)  # Font size 14px
        list_widget.setFont(font)

        # Set border radius for the list widget
        style = "border: 1px solid rgba(255,255,255,40); border-radius: 2px;"

        # Set text color
        text_color = QColor(255, 255, 255)  # White text color
        list_widget.setStyleSheet(f"{style} color: {text_color.name()};")

        # Add items to QListWidget
        for original, translated in self.recent_translations:
            item = QListWidgetItem(f"{original} -> {translated}")
            list_widget.addItem(item)

        # Add QListWidget to the dialog window
        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
