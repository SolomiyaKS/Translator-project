import sys
from PyQt6.QtWidgets import QApplication
from app.ui_loader import MW

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
