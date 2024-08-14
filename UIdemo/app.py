import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #self.button_is_checked = True
        
        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        #button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        #button.setChecked(self.button_is_checked)
        
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)
        
        #Also change window title
        self.setWindowTitle("My Oneshot App")
    
    '''def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print(self.button_is_checked)'''

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

