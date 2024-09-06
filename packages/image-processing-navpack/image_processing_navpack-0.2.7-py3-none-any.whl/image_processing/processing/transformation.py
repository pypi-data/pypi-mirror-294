from skimage.color import rgb2gray
from skimage.metrics import structural_similarity
from skimage.transform import resize
import numpy as np

def resize_image(image, target_shape):
    """
    Resizes the image to the target shape.
    """
    return resize(image, target_shape, anti_aliasing=True)

def normalize_image(image):
    """
    Normalizes the image to the range [0, 1].
    """
    if image.dtype == np.uint8:
        # Image is already in the range [0, 255]
        image = image / 255.0
    elif image.dtype in [np.float32, np.float64]:
        # If the image is in the range [0, 1], no need to normalize
        if image.max() > 1.0:
            # If the image has values greater than 1.0, normalize to [0, 1]
            image = (image - image.min()) / (image.max() - image.min())
    else:
        raise ValueError("Unsupported image type for normalization.")
    return image

def find_difference(image1, image2):
    """
    Computes the difference between two images.
    """
    # Convert to grayscale if images are in RGB format
    gray_image1 = rgb2gray(image1) if len(image1.shape) == 3 and image1.shape[2] == 3 else image1
    gray_image2 = rgb2gray(image2) if len(image2.shape) == 3 and image2.shape[2] == 3 else image2
    
    # Resize images to the same shape if they are different
    if gray_image1.shape != gray_image2.shape:
        gray_image2 = resize_image(gray_image2, gray_image1.shape)
    
    # Normalize images to range [0, 1]
    gray_image1 = normalize_image(gray_image1)
    gray_image2 = normalize_image(gray_image2)
    
    # Calculate the absolute difference between the images
    abs_difference_image = np.abs(gray_image1 - gray_image2)
    
    # Normalize the difference image to range [0, 1]
    abs_difference_image = normalize_image(abs_difference_image)
    
    # Compute structural similarity (if needed for other purposes)
    score, _ = structural_similarity(gray_image1, gray_image2, full=True, data_range=1)
    print("Similarity of the images:", score)
    
    return abs_difference_image
