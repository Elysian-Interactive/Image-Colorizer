import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QMessageBox, QFileDialog)
# TODO : Use MessageBoxes

class ImageColorizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        # Initial Window Setup
        self.setGeometry(100, 100, 1152, 648)
        self.setWindowTitle("Empty Window")
        
        # Creating the function to setup the buttons
        self.setupButtons()
        
        self.show()

    def setupButtons(self):
        
        # Creating vertical layout to house all other layout
        window_layout = QVBoxLayout()
        
        # Various Buttons for different functions
        open_img_btn = QPushButton("Open Image", self)
        open_img_btn.clicked.connect(self.openImageFiles)
        
        colorize_img_btn = QPushButton("Colorize", self)
        
        save_img_btn = QPushButton("Save Image", self)
        save_img_btn.clicked.connect(self.saveImageFiles)
        
        # Button Layout to store these buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(100)
        button_layout.addWidget(open_img_btn)
        button_layout.addWidget(colorize_img_btn)
        button_layout.addWidget(save_img_btn)
        
        # Adding all other layouts in the main layout
        window_layout.addStretch()
        window_layout.addLayout(button_layout)
        
        # Setting the main layout for the app
        self.setLayout(window_layout)
    
    # Function to load the images and pass them for conversion
    def openImageFiles(self):
        # Getting the image file to load the data
        file_name = QFileDialog.getOpenFileName(self,"Browse Image", "", "All Files (*) ;; Image Files (*.png *.jpg *.jpeg)")
        
        # Checking if the file is valid
        if file_name:
            print(file_name)
    
    # Function to save the images after they have been converted
    def saveImageFiles(self):
        # Getting the path where user wish to store the image
        file_name = QFileDialog.getSaveFileName(self, "Save ImageE", "", "All Files (*)")
        
        # Checking if the filepath is valid and creating it
        if file_name:
            print(file_name)
    
    # Function where actual colorization takes place
    def colorizeImage(self):
        pass
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageColorizer()
    sys.exit(app.exec_())
    