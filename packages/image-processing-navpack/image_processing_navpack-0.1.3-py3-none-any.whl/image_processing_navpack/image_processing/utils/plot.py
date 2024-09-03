import matplotlib.pyplot as plt

def plot_image(image, title='Image'):
    """
    Plots an image with a title.
    """
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.show()
