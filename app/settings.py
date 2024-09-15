import json

class SettingsManager:
    def __init__(self, window):
        self.window = window
        self.theme = 'light'

    def save_settings(self):
        settings = {
            'window_width': self.window.width(),
            'window_height': self.window.height(),
            'combo_1': self.window.combo_1.currentText(),
            'combo_2': self.window.combo_2.currentText(),
            'theme': self.theme
        }
        with open('resources/settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('resources/settings.json', 'r') as f:
                settings = json.load(f)
                self.window.combo_1.setCurrentText(settings.get('combo_1', 'english'))
                self.window.combo_2.setCurrentText(settings.get('combo_2', 'german'))
                self.window.resize(settings.get('window_width', 800), settings.get('window_height', 600))
                self.theme = settings.get('theme', 'light')
                self.apply_theme()
        except FileNotFoundError:
            self.window.combo_1.setCurrentText("english")
            self.window.combo_2.setCurrentText("german")
            self.theme = 'light'
            self.apply_theme()

    def toggle_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'
        self.apply_theme()

    def apply_theme(self):
        if self.theme == 'light':
            self.window.setStyleSheet("""
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
            self.window.setStyleSheet("""
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
