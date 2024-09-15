from PyQt6.QtWidgets import QMainWindow, QPushButton, QComboBox, QTextEdit, QMessageBox, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from app.translator_logic import TranslatorLogic
from app.settings import SettingsManager

class MW(QMainWindow):
    def __init__(self):
        super(MW, self).__init__()

        # Load the .ui file
        uic.loadUi("resources/translator.ui", self)
        self.setWindowTitle("Translator APP")

        # Set window icon
        self.setWindowIcon(QIcon("resources/icon.png"))

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

        # Translator logic
        self.translator_logic = TranslatorLogic(self)

        # Settings manager
        self.settings_manager = SettingsManager(self)

        # Connect signals to slots
        self.l_button.clicked.connect(self.translator_logic.clear)
        self.t_button.clicked.connect(self.translator_logic.translate)
        self.r_button.clicked.connect(self.translator_logic.show_recent)
        self.c_button.clicked.connect(self.translator_logic.copy_text)
        self.theme_button.clicked.connect(self.settings_manager.toggle_theme)

        # Initialize settings and shortcuts
        self.settings_manager.load_settings()
        self.translator_logic.init_shortcuts()

        # Auto-detect language when text changes in textEdit_1
        self.txt_1.textChanged.connect(self.translator_logic.auto_detect_language)

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        event.accept()
