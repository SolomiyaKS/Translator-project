import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTextEdit, QMessageBox, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QIcon, QKeySequence, QAction
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
        self.theme_button = self.findChild(QPushButton, "theme")
        self.combo_1 = self.findChild(QComboBox, "comboBox_1")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")
        self.txt_1 = self.findChild(QTextEdit, "textEdit_1")
        self.txt_2 = self.findChild(QTextEdit, "textEdit_2")

        # Connect signals to slots
        self.l_button.clicked.connect(self.clear)
        self.t_button.clicked.connect(self.translate)
        self.r_button.clicked.connect(self.show_recent)
        self.c_button.clicked.connect(self.copy_text)
        self.theme_button.clicked.connect(self.toggle_theme)  # Connect the theme button

        # Add languages to the combo boxes
        self.languages = LANGUAGES
        self.language_list = list(self.languages.values())
        self.combo_1.addItems(self.language_list)
        self.combo_2.addItems(self.language_list)

        # Make textEdit_2 read-only
        self.txt_2.setReadOnly(True)

        # List to store recent translations
        self.recent_translations = []

        # Load settings
        self.load_settings()

        # Initialize keyboard shortcuts
        self.init_shortcuts()

    def save_settings(self):
        settings = {
            'window_width': self.width(),
            'window_height': self.height(),
            'combo_1': self.combo_1.currentText(),
            'combo_2': self.combo_2.currentText(),
            'theme': self.theme  # Save the current theme
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
                self.theme = settings.get('theme', 'light')  # Load the theme
                self.apply_theme()
        except FileNotFoundError:
            self.combo_1.setCurrentText("english")
            self.combo_2.setCurrentText("german")
            self.theme = 'light'
            self.apply_theme()

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

    def toggle_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'
        self.apply_theme()

    def apply_theme(self):
        if self.theme == 'light':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgb(255, 255, 255);
                }
                QTextEdit, QComboBox, QPushButton, QListWidget {
                    background-color: rgba(162, 162, 162, 30);
                    color: black;
                    border: 1px solid rgba(162, 162, 162, 40);
                    border-radius: 2px;
                }
                QTextEdit:focus, QComboBox:focus, QPushButton:focus {
                    border: 2px solid #00bfff;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgb(53, 53, 53);
                }
                QTextEdit, QComboBox, QPushButton, QListWidget {
                    background-color: rgba(42, 42, 42, 30);
                    color: white;
                    border: 1px solid rgba(42, 42, 42, 40);
                    border-radius: 2px;
                }
                QTextEdit:focus, QComboBox:focus, QPushButton:focus {
                    border: 2px solid #00bfff;
                }
            """)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
