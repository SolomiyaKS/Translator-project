import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTextEdit, QMessageBox, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QColor, QIcon, QKeySequence, QAction
from PyQt6 import uic
from googletrans import Translator, LANGUAGES
import json

class MW(QMainWindow):
    def __init__(self):
        super(MW, self).__init__()

        # Load the .ui file
        uic.loadUi("translator.ui", self)
        self.setWindowTitle("Translator APP")

        # Set window icon
        self.setWindowIcon(QIcon("icon.png"))

        # Widgets
        self.t_button = self.findChild(QPushButton, "translate_btn")
        self.l_button = self.findChild(QPushButton, "clear_btn")
        self.r_button = self.findChild(QPushButton, "recent_btn")
        self.c_button = self.findChild(QPushButton, "copy_btn")
        self.combo_1 = self.findChild(QComboBox, "comboBox_1")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")
        self.txt_1 = self.findChild(QTextEdit, "textEdit_1")
        self.txt_2 = self.findChild(QTextEdit, "textEdit_2")

        # Connect signals to slots
        self.l_button.clicked.connect(self.clear)
        self.t_button.clicked.connect(self.translate)
        self.r_button.clicked.connect(self.show_recent)
        self.c_button.clicked.connect(self.copy_text)

        # Add languages to the combo boxes
        self.languages = LANGUAGES
        self.language_list = list(self.languages.values())
        self.combo_1.addItems(self.language_list)
        self.combo_2.addItems(self.language_list)

        # Make textEdit_2 read-only
        self.txt_2.setReadOnly(True)

        # Load settings
        self.load_settings()

        # List to store recent translations
        self.recent_translations = []

        # Initialize keyboard shortcuts
        self.init_shortcuts()

    def save_settings(self):
        settings = {
            'window_width': self.width(),
            'window_height': self.height()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.combo_1.setCurrentText(settings.get('combo_1', 'english'))
                self.combo_2.setCurrentText(settings.get('combo_2', 'german'))
                self.resize(settings.get('window_width', 800), settings.get('window_height', 600))
        except FileNotFoundError:
            self.combo_1.setCurrentText("english")
            self.combo_2.setCurrentText("german")

    def clear(self):
        self.txt_1.clear()
        self.txt_2.clear()

    def copy_text(self):
        QApplication.clipboard().setText(self.txt_2.toPlainText())

    def translate(self):
        try:
            translator = Translator()
            from_language_key = next(key for key, value in self.languages.items() if value == self.combo_1.currentText())
            to_language_key = next(key for key, value in self.languages.items() if value == self.combo_2.currentText())
            words = self.txt_1.toPlainText()
            translated_text = translator.translate(words, src=from_language_key, dest=to_language_key).text
            self.txt_2.setText(translated_text)
            self.save_recent_translation(words, translated_text)
        except Exception as e:
            QMessageBox.about(self, "Translator", str(e))

    def save_recent_translation(self, original, translated):
        if not self.recent_translations or self.recent_translations[-1] != (original, translated):
            self.recent_translations.append((original, translated))
            if len(self.recent_translations) > 10:
                self.recent_translations.pop(0)

    def show_recent(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Recent Translations")
        dialog.setGeometry(450, 200, 400, 200)
        layout = QVBoxLayout()
        list_widget = QListWidget()
        font = QFont()
        font.setPointSize(14)
        list_widget.setFont(font)
        list_widget.setStyleSheet("border: 2px solid rgba(162,162,162,40); border-radius: 2px; color: black;")
        for original, translated in self.recent_translations:
            list_widget.addItem(QListWidgetItem(f"{original} -> {translated}"))
        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec()

    def init_shortcuts(self):
        self.create_shortcut("Ctrl+L", self.clear)
        self.create_shortcut("Ctrl+R", self.show_recent)
        self.create_shortcut("Ctrl+T", self.translate)
        self.create_shortcut("Ctrl+C", self.copy_text)

    def create_shortcut(self, key_sequence, callback):
        action = QAction(self)
        action.setShortcut(QKeySequence(key_sequence))
        action.triggered.connect(callback)
        self.addAction(action)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
