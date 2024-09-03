from skimage.color import rgb2gray
from skimage.metrics import structural_similarity
from skimage.transform import resize

def resize_image(image, target_shape):
    """
    Resizes the image to the target shape.
    """
    return resize(image, target_shape, anti_aliasing=True)

def find_difference(image1, image2):
    """
    Computes the difference between two images.
    """
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    
    # Normalize images to range [0, 1]
    gray_image1 = (gray_image1 - gray_image1.min()) / (gray_image1.max() - gray_image1.min())
    gray_image2 = (gray_image2 - gray_image2.min()) / (gray_image2.max() - gray_image2.min())
    
    # Compute structural similarity
    score, difference_image = structural_similarity(gray_image1, gray_image2, full=True, data_range=1)
    print("Similarity of the images:", score)
    
    return difference_image
