import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QMessageBox, QFileDialog)
from Colorizer import Colorizer
import cv2

# TODO : Use MessageBoxes

class ImageColorizer(QWidget):
    def __init__(self):
        # Calling the parent constructur
        super().__init__()
        
        # Initializing the colorizer
        self.colorizer = Colorizer()
        self.colorizer.setPath('Model/colorization_deploy_v2.prototxt', 'Model/colorization_release_v2.caffemodel', 'Model/pts_in_hull.npy')
        self.colorizer.loadModel()
        
        # Setting up the UI
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
        colorize_img_btn.clicked.connect(self.colorizeImage)
        
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
            self.gray_image = file_name[0]
            print("Gray Image Succesfully opened")
    
    # Function to save the images after they have been converted
    def saveImageFiles(self):
        # Getting the path where user wish to store the image
        file_name = QFileDialog.getSaveFileName(self, "Save ImageE", "", "All Files (*)")
        
        # Checking if the filepath is valid and creating it
        if file_name:
            cv2.imwrite(file_name[0], self.color_image)
            print("Color image saved")
    
    # Function where actual colorization takes place
    def colorizeImage(self):
        self.color_image = self.colorizer.colorize(self.gray_image)
        print("Converted to color image")
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageColorizer()
    sys.exit(app.exec_())
    