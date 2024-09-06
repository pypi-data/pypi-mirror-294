from skimage.exposure import match_histograms
from skimage.util import img_as_ubyte

def transfer_histogram(image1, image2):
    """
    Transfers the histogram from image1 to image2.
    """
    # Ensure both images are in 8-bit format
    image1 = img_as_ubyte(image1)
    image2 = img_as_ubyte(image2)
    return match_histograms(image2, image1, channel_axis=-1)
