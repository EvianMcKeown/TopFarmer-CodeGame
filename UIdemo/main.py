from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QPushButton, QApplication, QWidget, QMainWindow
import sys #for access to command line args

# Subclass QMainWindow to customize it
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")
        self.setFixedSize(QSize(400, 300))
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(900, 720))
        
        # set central widget of window
        self.setCentralWidget(button)

# only one QApplication instance per application
app = QApplication(sys.argv)

# create Qt Widget, which will be the application window
window = MainWindow()
window.show() # Windows are hidden by default

# start event loop
app.exec()