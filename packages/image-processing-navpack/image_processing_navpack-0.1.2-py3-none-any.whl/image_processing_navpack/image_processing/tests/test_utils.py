import os
import pytest
import numpy as np
from image_processing.utils.io import read_image, save_image
from image_processing.utils.plot import plot_image

def test_io():
    img_folder = 'image_processing/imgs'
    
    # Paths for testing
    image1_path = os.path.join(img_folder, 'imagem1.jpg')
    output_path = os.path.join(img_folder, 'output_test.jpg')

    image1 = read_image(image1_path)
    assert image1 is not None

    save_image(image1, output_path)
    assert os.path.exists(output_path)

    # Optionally, you can include assertions to check image properties

    # Clean up
    os.remove(output_path)
