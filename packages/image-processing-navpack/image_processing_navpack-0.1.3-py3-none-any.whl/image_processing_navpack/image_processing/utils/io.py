import os
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte

def read_image(path, is_gray=False):
    """
    Reads an image from the specified path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: '{path}'")
        
    image = imread(path, as_gray=is_gray)
    if not is_gray and len(image.shape) == 2:
        from skimage.color import gray2rgb
        image = gray2rgb(image)
    return image

def save_image(image, path):
    """
    Saves the image to the specified path.
    """
    # Convert the image to 8-bit unsigned integer format
    image = img_as_ubyte(image)
    imsave(path, image)
