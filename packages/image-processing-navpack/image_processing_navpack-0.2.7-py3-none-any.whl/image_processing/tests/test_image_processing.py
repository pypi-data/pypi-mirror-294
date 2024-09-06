import os
import pytest
from image_processing.utils.io import read_image, save_image
from image_processing.utils.plot import plot_result, plot_histograms_side_by_side
from image_processing.processing.combination import transfer_histogram
from image_processing.processing.transformation import rgb2gray

@pytest.fixture
def setup_images():
    img_folder = 'image_processing/imgs'
    image1 = read_image(os.path.join(img_folder, 'imagem1.jpg'))
    image2 = read_image(os.path.join(img_folder, 'imagem2.jpg'))
    return image1, image2

def test_transfer_histogram(setup_images):
    image1, image2 = setup_images
    result_img = transfer_histogram(image1, image2)
    save_image(result_img, 'test_image_transferred.jpg')
    assert os.path.exists('test_image_transferred.jpg')

def test_convert_to_gray(setup_images):
    image1, _ = setup_images
    gray_image1 = rgb2gray(image1)
    gray_image1 = (gray_image1 - gray_image1.min()) / (gray_image1.max() - gray_image1.min()) * 255
    save_image(gray_image1, 'test_image1_gray.jpg')
    assert os.path.exists('test_image1_gray.jpg')

if __name__ == "__main__":
    pytest.main()
