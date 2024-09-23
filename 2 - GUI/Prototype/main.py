import sys
from PyQt5.QtWidgets import QApplication, QWidget

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        self.setGeometry(100, 100, 1152, 648)
        self.setWindowTitle("Empty Window")
        self.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewWindow()
    sys.exit(app.exec_())
    