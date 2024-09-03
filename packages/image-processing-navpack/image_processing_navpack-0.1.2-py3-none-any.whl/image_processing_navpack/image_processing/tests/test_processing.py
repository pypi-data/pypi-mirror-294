import os
import pytest
import numpy as np
from image_processing.utils.io import read_image
from image_processing.processing.transformation import resize_image, find_difference
from image_processing.processing.combination import transfer_histogram

def test_image_processing():
    img_folder = 'image_processing/imgs'
    
    # Paths for testing
    image1_path = os.path.join(img_folder, 'imagem1.jpg')
    image2_path = os.path.join(img_folder, 'imagem2.jpg')

    image1 = read_image(image1_path)
    image2 = read_image(image2_path)

    assert image1 is not None
    assert image2 is not None

    height, width = image1.shape[:2]
    image2_resized = resize_image(image2, (height, width, image2.shape[2]))

    difference_image = find_difference(image1, image2_resized)
    assert difference_image is not None
    assert difference_image.shape == (height, width)

    histogram_matched_image = transfer_histogram(image1, image2_resized)
    assert histogram_matched_image is not None
    assert histogram_matched_image.shape == image2_resized.shape
