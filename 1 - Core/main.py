import numpy as np
import cv2

# Step 1 : To define all the paths

prototxt_path = 'colorization_deploy_v2.prototxt'
model_path = 'colorization_release_v2.caffemodel'
kernel_path = 'pts_in_hull.npy'
image_path = 'gray.jpg'

# Now to define and load the pre-trained neural network
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
# These are clustering points which are useful for the model
points = np.load(kernel_path)

# Now we need to reshape them to 1x1 for a CNN
points = points.transpose().reshape(2,313, 1, 1)

# now we will get the specific layer type
# Here we are working with the LAB color space
# LAB -> Lightness and a* and b* define the color values
# we are loading the centers for the channel quantization of a and b 
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype = 'float32')]
# then we created blob which are binary large objects

# Next step is to load the gray image, normalize it and then convert it to LAB color space
bw_image = cv2.imread(image_path)
normalized = bw_image.astype("float32") / 255.0 # normalizing to 0 and 1
lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

# Now we need to resize the image bcz the model is trained to convert 224 x 224 images
resized = cv2.resize(lab, (224,224))
# now we will split the channels
L = cv2.split(resized)[0]
L -= 50 # we subtract the mean value and you can play with it to affect the result

# Now since we only have the L value we will use the model to generate a and b color values
net.setInput(cv2.dnn.blobFromImage(L))

# now to store the image
ab = net.forward()[0, :, :, :].transpose((1,2,0))

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

# Now to display the images
cv2.imshow("BW Image", bw_image)
cv2.imshow("Colorized", colorized)
cv2.waitKey(0)
cv2.destroyAllWindows()
