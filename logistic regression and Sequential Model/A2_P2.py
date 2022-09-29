import tensorflow as tf
from tensorflow.keras import *
import numpy as np

"""
-----------------------------------------------------------------------------------------------
Problem 2 Code a sequential model with architecture given in assignment description, 
            and fit your model with given data
-----------------------------------------------------------------------------------------------
"""

"""
-----------------------------------------------------------------------------------------------
Step 1. Load mnist dataset. [5 points]
-----------------------------------------------------------------------------------------------
"""

(x_train, _), (x_test, _) = ____________________

"""
pre-processing procedure.
DON'T change code at this section
"""
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train: np.ndarray
x_test: np.ndarray
image_size: int = np.shape(x_train)[1]
n_channel = 1

x_train = x_train.reshape(x_train.shape[0], image_size, image_size, n_channel)
x_test = x_test.reshape(x_test.shape[0], image_size, image_size, n_channel)

x_train_noise: np.ndarray = x_train + 0.25 * np.random.normal(0.0, 1.0, x_train.shape)
x_test_noise: np.ndarray = x_test + 0.25 * np.random.normal(0.0, 1.0, x_test.shape)

# Input of your model for training and testing
x_train_noise = np.clip(x_train_noise, 0.0, 1.0)
x_test_noise = np.clip(x_test_noise, 0.0, 1.0)

"""
-----------------------------------------------------------------------------------------------
Step 2. Code you sequential model here. [10 points]
Activation function for convolutional layers, fully connected layers and convolutional transpose layers:
Layers < 12: relu
Layers == 12: sigmoid

Architecture:
Layer 1 - Convolutional layer [number of filters=32, kernel size=(4, 4)]
Layer 2 - Max polling layer [pool_size=(2, 2)]
Layer 3 - Convolutional layer [number of filters=64, kernel size=(4, 4)]
Layer 4 - Max polling layer [pool_size=(2, 2)]
Layer 5 - Fully connected layer [number of units=512]
Layer 6 - Fully connected layer [number of units=10]
Layer 7 - Fully connected layer [number of units=512]
Layer 8 - Convolutional Transpose layer [number of filters=64, kernel size=(3, 3)]
Layer 9 - Upsampling layer [size=(2, 2)]
Layer 10 - Convolutional Transpose layer [number of filters=32, kernel size=(3, 3)]
Layer 11 - Upsampling layer [size=(2, 2)]
Layer 12 - Convolutional Transpose layer [number of filters=1, kernel size=1]

Use tf.keras.utils.plot_model to plot your model with the shapes of each layer
    into a png file named P1-model-[Your_access_ID].png
-----------------------------------------------------------------------------------------------
"""

model = Sequential()

# adding layers into the model
# doesn't mean just one line code here, just to remind to write codes here.

utils.plot_model(model, "model.png", show_shapes=True)

"""
-----------------------------------------------------------------------------------------------
Step 3. Compile train your model. [5 points]
Optimizer: Adam optimizer (use default parameters)
Loss: bianry crossentropy with specific name 'loss'
-----------------------------------------------------------------------------------------------
"""
optimizer = ____________________
loss_fn = ____________________
model.compile(____________________)

"""
-----------------------------------------------------------------------------------------------
Step 4. Fit your model and save it to P1-[Your_access_ID].h5. [5 points]
Use x_train_noise as input, and x_train as target;
set batch_size as 36 and number of epochs as 10;
Use EarlyStopping callback to monitor loss and stop training early with delta=0.01
Use the tuple of x_test_noise and x_test as the validation data
-----------------------------------------------------------------------------------------------
"""
early_stopping_callback = ____________________
model.fit(____________________)

"""
-----------------------------------------------------------------------------------------------
Remember to submit results to Canvas. [5 points]
-----------------------------------------------------------------------------------------------
"""

"""
-----------------------------------------------------------------------------------------------
DON'T modify code below
-----------------------------------------------------------------------------------------------
"""
# output original and modified images
batch_size = 16
sample_idx = np.random.randint(low=0, high=10000, size=batch_size)
r_samples = x_test_noise[sample_idx, :, :, :]
rec_samples = model.predict(x=r_samples)
fig = np.zeros(shape=(image_size*2, image_size*batch_size, 1))
r_samples = r_samples * 255
rec_samples = rec_samples * 255

for idx in range(batch_size):
    fig[:image_size, idx*image_size: (idx+1)*image_size, :] = r_samples[idx, :, :]
    fig[image_size:, idx * image_size: (idx + 1) * image_size, :] = rec_samples[idx, :, :]

fig = fig.reshape(image_size*2, image_size*batch_size, 1)
fig = tf.image.encode_jpeg(fig)
tf.io.write_file("out.jpg", fig)
