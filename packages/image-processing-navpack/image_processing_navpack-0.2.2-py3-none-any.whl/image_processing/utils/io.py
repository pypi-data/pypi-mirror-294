import os
import numpy as np
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte
from skimage.color import gray2rgb
from image_processing.processing.transformation import normalize_image

def read_image(path, is_gray=False):
    """
    Reads an image from the specified path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: '{path}'")
    
    # Read the image
    image = imread(path, as_gray=is_gray)
    
    # Convert grayscale to RGB if needed
    if not is_gray and len(image.shape) == 2:
        image = gray2rgb(image)
    
    return image

def save_image(image, filepath):
    """
    Saves the image to the specified file path.
    """
    # Normalize image to [0, 1] if needed
    if image.dtype in [np.float32, np.float64]:
        image = normalize_image(image)  # Normalize to [0, 1]

    # Convert to uint8 format for saving
    if image.max() > 1.0:  # If normalized to [0, 255]
        image = np.clip(image, 0, 255)
    image = img_as_ubyte(image)

    # Save the image
    imsave(filepath, image)
