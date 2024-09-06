import os
import pytest
from image_processing.utils.io import read_image
from image_processing.processing.transformation import find_difference

# Caminho relativo para a pasta imgs
IMG_DIR = os.path.join(os.path.dirname(__file__), '../imgs')

def test_find_difference():
    image1_path = os.path.join(IMG_DIR, 'imagem1.jpg')
    image2_path = os.path.join(IMG_DIR, 'imagem2.jpg')
    
    image1 = read_image(image1_path)
    image2 = read_image(image2_path)
    
    difference_image = find_difference(image1, image2)
    
    assert difference_image is not None
    assert difference_image.min() >= 0 and difference_image.max() <= 1  # Ensure image is in correct range
