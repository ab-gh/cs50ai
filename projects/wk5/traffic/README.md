# CS50ai Week 5: traffic

This README explains the process of experimentation to obtain the optimal convolutional neural network for GTSRB image classification

## Initial configuration

I started with a basic initial baseline configuration with an accuracy of at least 0.5 (better than random). The following layers were set up using TensorFlow's Keras API:

1. `layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))`
   1. A 2D convolutional layer, using 32 filters with a (3, 3) kernel size, and ReLU activation.
2. `layers.Flatten()`
   1. Flattens the previous layer.
3. `layers.Dense(NUM_CATEGORIES, activation="softmax")`
   1. Regular densely-connected final output layer with the correct output units, and with softmax activation to normalise vectors.

This intitial configuration worked reasonably well. After 10 training epochs, the model was tested and resulted in an accuracy of 97.86%, and a loss rate of 1.1732. This model has a reasonably high accuracy, but the loss can be improved.

## Understanding CNNs

After some research, I found a [good article explaining how CNNs work with image recognition](https://medium.com/@sdoshi579/convolutional-neural-network-learn-and-apply-3dac9acfe2b6). A typical CNN consists of a "Feature Extraction" section, followed by a "Classification" section. The first section consists of multiple combinations of Convolutional layers with ReLU activation, followed by pooling layers. This sequence attempts to mimic the human brain analyzing the rough outline and general overall features of an image, rather than looking at each millimeter of a picture as a separate idea. Pooling layers also help to make the model more efficient, by reducing the amount of data that moves through the entire model. The second "Classification" section then uses a flatten layer to convert the image's 2D vectors into flat 1D vectors, some fully connected dense layers, and a final Softmax output layer. Softmax will normalize each of the node vectors, so we can treat this final layer as a probabilistic classification. 

This article also outlines the use of Dropout layers. These layers randomly "disconnect" connections between nodes based on a given probability, which helps prevent over-reliance on certain node connections. 

### Feature Extraction

The feature extraction section is constructed of multiple sequences of the following layers:

1. Convolutional 2D layer, with 3x3 kernels and ReLU activation
2. A second convolutional 2D layer of the same type
3. A Pooling layer using 2x2 pools
4. A dropout layer with 20% probability

### Classification

The classification section is constructed of multiple sequences of the following layers:

1. A dense layer with ReLU activation
2. A dropout layer with 30% probability

The classification layer will end with a dense output layer with softmax activation, with the number of nodes corresponding to the number of classification types.

## Improvement attempts

The attempts began with one sequence of both the Feature Extraction layer and Classification layer, initially using 8 filters for the convolutional layer, and 2048 nodes for the dense layer.

```
# Feature extraction
layers.Conv2D(8, (3, 3), activation='relu'),
layers.Conv2D(8, (3, 3), activation='relu'),
layers.Dropout(0.2),
layers.MaxPooling2D(2, 2),
layers.Flatten(),
# Classification
layers.Dense(2048, activation='relu'),
layers.Dropout(0.3)
layers.Dense(NUM_CATEGORIES, activation='softmax')
```

This first attempt resulted in a greatly improved loss rate of 0.2123, but a slightly reduced accuracy rate of 96.04%

The second attempt involved adding in another sequence in both sections, doubling the number of convolutional filters and adding another dense layer with half the proceeding nodes. Batch normalisation was also added between convolutional layers in the first section. It resulted in an increased accuracy rate of 98.55%, and a reduced loss rate 0.0518, greatly improving on the previous attempt.

The final attempt again doubled the number of filters used, and used a dense layer of 128 nodes before the final output layer. The final of the two convolutional 2D layers in the section was skipped, as the images could not be reshaped at that level. This resulted in a *worse* accuracy of 94.76%, and a worse loss rate of 0.1653. 

To identify the cause of the reduction in accuracy, I removed the final convolutional layer, which resulted in an almost-equal result of 98.5% accuracy and 0.0556 loss rate. This indicates that the extra convolutional filter layer was actually inhibiting performance, not increasing it. 

Therefore, by using the CNN architecture described by the above article, the model accuracy was increased from 97.86% to 98.5%, and the loss rate reduced from 1.1732 to 0.0556, a clear improvement.
