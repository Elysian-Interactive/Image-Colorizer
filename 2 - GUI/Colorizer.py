import numpy as np
import cv2

class Colorizer:
    def __init__(self):
        # These are the important paths to be used by Colorizer
        self.prototxt_path = None
        self.model_path = None
        self.kernel_path = None
        
        # This variable will represent the loaded model
        self.net = None
    
    def setPath(self, prototxt_path, model_path, kernel_path):
        # Setting the paths
        self.prototxt_path = prototxt_path
        self.model_path = model_path
        self.kernel_path = kernel_path
        
    def loadModel(self):
        # Now to define and load the pre-trained neural network
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)
        # These are clustering points which are useful for the model
        points = np.load(self.kernel_path)
        # Now we need to reshape them to 1x1 for a CNN
        points = points.transpose().reshape(2,313, 1, 1)
        # now we will get the specific layer type
        self.net.getLayer(self.net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
        self.net.getLayer(self.net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype = 'float32')]
        # then we created blob which are binary large objects
    
    def colorize(self, image_path):
        # Next step is to load the gray image, normalize it and then convert it to LAB color space, as the model only works in this color space
        bw_image = cv2.imread(image_path)
        normalized = bw_image.astype("float32") / 255.0 # normalizing to 0 and 1
        lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)
       
       # Now we need to resize the image bcz the model is trained to convert 224 x 224 images
        resized = cv2.resize(lab, (224,224))
        # now we will split the channels
        L = cv2.split(resized)[0]
        L -= 50 # we subtract the mean value and we can play with it to affect the result
       
       # Now since we only have the L value we will use the model to generate a and b color values
        self.net.setInput(cv2.dnn.blobFromImage(L))
        # now to store the generated ab channel
        ab = self.net.forward()[0, :, :, :].transpose((1,2,0))
        # and then we will resize the image back to the its original dimensions
        ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
        
        # now we will get the lightness values back
        L = cv2.split(lab)[0]
        # and now we will combine all the channels
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis = 2)
        # now to again convert it to bgr space to display
        colorized = cv2.cvtColor(colorized , cv2.COLOR_LAB2BGR)
        # now to scale it back as we have normalized it
        colorized = (255.0 * colorized).astype("uint8")
        
        # Now that we have generated our image we return it
        return colorized