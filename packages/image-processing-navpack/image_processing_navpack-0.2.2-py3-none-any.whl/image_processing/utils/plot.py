import numpy as np
import matplotlib.pyplot as plt

def plot_image(image, title='Image'):
    """
    Plots an image with a title.
    """
    plt.imshow(image, cmap='gray' if len(image.shape) == 2 else None)
    plt.title(title)
    plt.axis('off')
    plt.show()

def plot_result(*args):
    """
    Displays multiple images in a row.
    """
    number_images = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=number_images, figsize=(12, 4))
    
    if number_images == 1:
        axis = [axis]  # Ensure that axis is iterable if there is only one image

    names_lst = ['Image {}'.format(i + 1) for i in range(number_images)]
    for ax, name, image in zip(axis, names_lst, args):
        ax.set_title(name)
        ax.imshow(image, cmap='gray' if len(image.shape) == 2 else None)
        ax.axis('off')
    fig.tight_layout()
    plt.show()

def plot_histograms_side_by_side(image1, image2=None, transferred_image=None, titles=None):
    """
    Plots histograms for the images side by side.
    
    :param image1: The first image.
    :param image2: The second image (optional).
    :param transferred_image: The transferred histogram image (optional).
    :param titles: Titles for each histogram plot.
    """
    images = [image1]
    if image2 is not None:
        images.append(image2)
    if transferred_image is not None:
        images.append(transferred_image)

    fig, axs = plt.subplots(1, len(images), figsize=(15, 5))
    if len(images) == 1:
        axs = [axs]  # Ensure that axs is iterable if there's only one histogram

    for i, image in enumerate(images):
        hist, bin_edges = np.histogram(image.ravel(), bins=256, range=(0, 255))
        axs[i].plot(bin_edges[:-1], hist, lw=2)
        axs[i].set_xlabel('Pixel value')
        axs[i].set_ylabel('Frequency')
        axs[i].set_title(titles[i] if titles else f'Image {i+1}')
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()
