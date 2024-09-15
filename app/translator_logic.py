from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QAction, QKeySequence
from googletrans import Translator, LANGUAGES

class TranslationThread(QThread):
    translation_done = pyqtSignal(str)

    def __init__(self, words, from_language_key, to_language_key):
        super().__init__()
        self.words = words
        self.from_language_key = from_language_key
        self.to_language_key = to_language_key

    def run(self):
        try:
            translator = Translator()
            translated_text = translator.translate(self.words, src=self.from_language_key, dest=self.to_language_key).text
            self.translation_done.emit(translated_text)
        except Exception as e:
            self.translation_done.emit(f"Error: {str(e)}")


class DetectionThread(QThread):
    detection_done = pyqtSignal(str)

    def __init__(self, words):
        super().__init__()
        self.words = words

    def run(self):
        try:
            translator = Translator()
            detected_lang = translator.detect(self.words).lang
            self.detection_done.emit(detected_lang)
        except Exception as e:
            self.detection_done.emit(f"Error: {str(e)}")


class TranslatorLogic:
    def __init__(self, window):
        self.window = window
        self.languages = LANGUAGES
        self.language_list = list(self.languages.values())
        self.recent_translations = []

        # Таймер для автодетекції
        self.detect_language_timer = QTimer()
        self.detect_language_timer.setInterval(500)
        self.detect_language_timer.timeout.connect(self.perform_auto_detection)

        # Додавання мов у випадаючі списки
        self.window.combo_1.addItems(self.language_list)
        self.window.combo_2.addItems(self.language_list)

    def clear(self):
        self.window.txt_1.clear()
        self.window.txt_2.clear()

    def copy_text(self):
        QApplication.clipboard().setText(self.window.txt_2.toPlainText())

    def translate(self):
        try:
            from_language_key = next(key for key, value in self.languages.items() if value == self.window.combo_1.currentText())
            to_language_key = next(key for key, value in self.languages.items() if value == self.window.combo_2.currentText())
            words = self.window.txt_1.toPlainText()

            # Запускаємо потік для перекладу
            self.translation_thread = TranslationThread(words, from_language_key, to_language_key)
            self.translation_thread.translation_done.connect(self.on_translation_done)
            self.translation_thread.start()
        except Exception as e:
            QMessageBox.about(self.window, "Translator", str(e))

    def on_translation_done(self, translated_text):
        """Обробка результату перекладу."""
        self.window.txt_2.setText(translated_text)
        if not translated_text.startswith("Error"):
            self.save_recent_translation(self.window.txt_1.toPlainText(), translated_text)

    def save_recent_translation(self, original, translated):
        """Зберігає останні переклади."""
        if not self.recent_translations or self.recent_translations[-1] != (original, translated):
            self.recent_translations.append((original, translated))
            if len(self.recent_translations) > 10:
                self.recent_translations.pop(0)

    def show_recent(self):
        dialog = QDialog(self.window)
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

    def auto_detect_language(self):
        """Запускає таймер для автодетекції мови."""
        self.detect_language_timer.start()

    def perform_auto_detection(self):
        """Викликає автодетекцію після завершення таймера."""
        self.detect_language_timer.stop()  # Зупиняємо таймер після виконання

        words = self.window.txt_1.toPlainText()
        if not words.strip():
            return

        # Запускаємо потік для автодетекції мови
        self.detection_thread = DetectionThread(words)
        self.detection_thread.detection_done.connect(self.on_detection_done)
        self.detection_thread.start()

    def on_detection_done(self, detected_lang):
        """Обробка результату автодетекції."""
        if detected_lang.startswith("Error"):
            QMessageBox.about(self.window, "Language Detection", detected_lang)
        else:
            lang_name = self.languages.get(detected_lang, 'english')
            self.window.combo_1.setCurrentText(lang_name)

    def init_shortcuts(self):
        self.create_shortcut("Ctrl+L", self.clear)
        self.create_shortcut("Ctrl+R", self.show_recent)
        self.create_shortcut("Ctrl+T", self.translate)
        self.create_shortcut("Ctrl+C", self.copy_text)

    def create_shortcut(self, key_sequence, callback):
        action = QAction(self.window)
        action.setShortcut(QKeySequence(key_sequence))
        action.triggered.connect(callback)
        self.window.addAction(action)
