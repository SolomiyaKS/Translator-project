# **Translator APP with PyQt6**
Translator APP is a PyQt6-based desktop application that allows users to translate text between different languages using the _Google Translate API_. It provides a user-friendly interface with options to select source and target languages, clear text, copy translations to clipboard, and view recent translations.
___
## **Installation**
To run the Translator APP locally, follow these steps:
1. Clone the repository:
   
   ```
   git clone <repository-url>
   cd translator-app
   ```
2. Install dependencies:

   ```
   pip install PyQt6 googletrans==4.0.0-rc1
   ```
3. Run the application:

   ```
   python translator.py
   ```
____
## **Usage**
1. Interface Overview:
   + Text Input: Enter text to be translated in the left-hand QTextEdit field.
   + Translation Output: View translated text in the right-hand QTextEdit field.
   + Language Selection: Use the ComboBoxes to select the source and target languages.
   + Buttons: Click "Translate" to perform translation, "Clear" to clear text fields, "Recent" to view recent translations, and "Copy" to copy translated text to clipboard.
2. Keyboard Shortcuts:
   + Ctrl+L: Clear text fields.
   + Ctrl+T: Translate text.
   + Ctrl+R: View recent translations.
   + Ctrl+C: Copy translated text to clipboard.
3. Settings:
   + Application settings such as selected languages and window size are automatically saved and restored upon restart.
  ____
## **Acknowledgments**
- PyQt6: Python bindings for Qt, used for building the GUI.
- Googletrans: Google Translate API for performing translations.


