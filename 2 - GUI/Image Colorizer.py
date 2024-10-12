import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QMessageBox, QFileDialog)
from PyQt5.QtGui import QPixmap
from Colorizer import Colorizer
import cv2
import os
import glob

# TODO : Use MessageBoxes

class ImageColorizer(QWidget):
    def __init__(self):
        # Calling the parent constructur
        super().__init__()
        
        # Initializing the colorizer
        self.colorizer = Colorizer()
        self.colorizer.setPath('Model/colorization_deploy_v2.prototxt', 'Model/colorization_release_v2.caffemodel', 'Model/pts_in_hull.npy')
        self.colorizer.loadModel()
        
        # A counter to store the amount of files colorized
        self.image_count = int(self.readImageCount())
        
        # Variables for the displayed color and gray images
        self.gray_image = QLabel(self)
        self.color_image = QLabel(self)
        
        # Setting up the UI
        self.initializeUI()
    
    # Function to read processed image count data
    def readImageCount(self):
        file = open('Assets/count.data', 'r')
        count = file.read()
        file.close()
        
        return count
    
    # Function to write processed image count data
    def writeImageCount(self):
        file = open('Assets/count.data', 'w')
        file.write(str(self.image_count))
        file.close()
        
    
    def initializeUI(self):
        # Initial Window Setup
        self.setGeometry(100, 100, 1152, 648)
        self.setWindowTitle("Image Colorizer")
        
        # Creating the function to setup the buttons
        self.setupButtons()
        
        self.show()

    def setupButtons(self):
        
        # Creating vertical layout to house all other layout
        window_layout = QHBoxLayout()
        
        # Various Buttons for different functions
        open_img_btn = QPushButton("Open Image", self)
        open_img_btn.clicked.connect(self.openImageFiles)
        
        colorize_img_btn = QPushButton("Colorize", self)
        colorize_img_btn.clicked.connect(self.colorizeImage)
        
        save_img_btn = QPushButton("Save Image", self)
        save_img_btn.clicked.connect(self.saveImageFiles)
        
        # Different Layouts
        gray_image_layout = QVBoxLayout()
        gray_image_layout.addWidget(self.gray_image)
        gray_image_layout.addWidget(open_img_btn)
        
        colorize_layout = QVBoxLayout()
        colorize_layout.addStretch()
        colorize_layout.addWidget(colorize_img_btn)
        colorize_layout.addStretch()
        
        color_image_layout = QVBoxLayout()
        color_image_layout.addWidget(self.color_image)
        color_image_layout.addWidget(save_img_btn)
        
        # Adding all other layouts in the main layout
        window_layout.addLayout(gray_image_layout)
        window_layout.addLayout(colorize_layout)
        window_layout.addLayout(color_image_layout)
        
        # Setting the main layout for the app
        self.setLayout(window_layout)
    
    # Function to load the images and pass them for conversion
    def openImageFiles(self):
        # Getting the image file to load the data
        file_name = QFileDialog.getOpenFileName(self,"Browse Image", "", "All Files (*) ;; Image Files (*.png *.jpg *.jpeg)")
        
        # Checking if the file is valid
        if file_name:
            self.gray_image_path = file_name[0]
            self.displayGrayImage()
            print("Gray Image Succesfully opened")
    
    # Function to display the gray image on the screen
    def displayGrayImage(self):
        pixmap = QPixmap(self.gray_image_path)
        pixmap = pixmap.scaled(400,300)
        self.gray_image.setPixmap(pixmap)
    
    # Function to save the images after they have been converted
    def saveImageFiles(self):
        # Getting the path where user wish to store the image
        file_name = QFileDialog.getSaveFileName(self, "Save Image", "", "All Files (*)")
        
        # Checking if the filepath is valid and creating it
        if file_name:
            cv2.imwrite(file_name[0], self.generated_color_image)
            # print("Color image saved")
    
    # Function where actual colorization takes place
    def colorizeImage(self):
        self.generated_color_image = self.colorizer.colorize(self.gray_image_path)
        # Saving the generated image temporarily
        cv2.imwrite(str('Processed/' + str(self.image_count) + '.jpg'), self.generated_color_image)
        # Displaying the image on the screen
        self.displayColorImage()
        # Incrementing the counter
        self.image_count += 1
        #print("Converted to color image")
    
    # Function to display the color image on the screen
    def displayColorImage(self):
        image_path = str('Processed/' + str(self.image_count) + '.jpg')
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(400,300)
        self.color_image.setPixmap(pixmap)
        
    
    # Function to display the gray image after it has been opened
    # This function will delete the saved images generated in a session
    def clearData(self):
        pattern = "Processed/*.jpg"

        # Use glob to find all files that match the pattern
        files = glob.glob(pattern)

        # Loop through the list of files and delete each one
        for file in files:
            os.remove(file)
    
    # Function to clean up and store some variables
    def closeEvent(self, event):
        self.writeImageCount()
       # self.clearData()
        
    
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageColorizer()
    sys.exit(app.exec_())
    