import os
import pytest
from image_processing.utils.io import read_image, save_image
from image_processing.utils.plot import plot_image

# Caminho relativo para a pasta imgs
IMG_DIR = os.path.join(os.path.dirname(__file__), '../imgs')

def test_read_image():
    image_path = os.path.join(IMG_DIR, 'imagem1.jpg')
    image = read_image(image_path)
    
    assert image is not None
    assert image.shape[2] == 3  # Ensure it is an RGB image

def test_save_image():
    image_path = os.path.join(IMG_DIR, 'imagem1.jpg')
    image = read_image(image_path)
    save_path = os.path.join(IMG_DIR, 'saved_image.jpg')
    
    save_image(image, save_path)
    
    assert os.path.exists(save_path)
    saved_image = read_image(save_path)
    assert saved_image is not None
    assert saved_image.shape[2] == 3  # Ensure it is an RGB image
