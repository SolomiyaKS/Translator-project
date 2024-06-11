import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication([])

w = QWidget()
w.setWindowTitle("PyQt translator")
w.setGeometry(100, 100, 280, 80)

m = QLabel("<h1>Hello, World!</h1>", parent=w)
m.move(60, 15)

w.show()
sys.exit(app.exec())