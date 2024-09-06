import os
import pkg_resources
from image_processing.utils.io import read_image, save_image
from image_processing.utils.plot import plot_result, plot_histograms_side_by_side
from image_processing.processing.combination import transfer_histogram
from image_processing.processing.transformation import rgb2gray

def normalize_image(image):
    """
    Normalizes the image to the range [0, 255].
    """
    return (image - image.min()) / (image.max() - image.min()) * 255

def get_resource_path(filename):
    """
    Returns the absolute path to a resource file inside the package.
    """
    return pkg_resources.resource_filename(__name__, os.path.join('imgs', filename))

def main():
    while True:
        print("\nMenu:")
        print("1 - Transferir Histograma entre as Imagens")
        print("2 - Mostrar Imagens")
        print("3 - Converter Imagem1 para Cinza")
        print("4 - Mostrar Imagem1 em Cinza")
        print("5 - Histograma das Imagens")
        print("6 - Histograma da Imagem Cinza")
        print("0 - Sair")

        choice = input("Digite sua escolha: ").strip()

        if choice == '1':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            image2 = read_image(get_resource_path('imagem2.jpg'))
            result_img = transfer_histogram(image1, image2)
            save_image(result_img, get_resource_path('image_transferred.jpg'))
            print("Histograma transferido e imagem salva como 'image_transferred.jpg'.")

        elif choice == '2':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            image2 = read_image(get_resource_path('imagem2.jpg'))
            transferred_image = read_image(get_resource_path('image_transferred.jpg'))
            plot_result(image1, image2, transferred_image)
            print("Imagem1, Imagem2 e a imagem resultante foram exibidas.")

        elif choice == '3':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            gray_image1 = rgb2gray(image1)  # Converter para escala de cinza
            gray_image1 = normalize_image(gray_image1)  # Normalizar imagem em escala de cinza
            save_image(gray_image1, get_resource_path('imagem1_gray.jpg'))
            print("Imagem1 convertida para escala cinza e salva como 'imagem1_gray.jpg'.")

        elif choice == '4':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            gray_image1 = read_image(get_resource_path('imagem1_gray.jpg'))
            plot_result(image1, gray_image1)
            print("Imagem1 e a imagem em cinza foram exibidas.")

        elif choice == '5':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            image2 = read_image(get_resource_path('imagem2.jpg'))
            transferred_image = read_image(get_resource_path('image_transferred.jpg'))
            plot_histograms_side_by_side(image1, image2, transferred_image, 
                                         titles=['Histograma Imagem1', 'Histograma Imagem2', 'Histograma Imagem Transferida'])
            print("Histograma das Imagens1, Imagem2 e a imagem gerada foram exibidos lado a lado.")

        elif choice == '6':
            image1 = read_image(get_resource_path('imagem1.jpg'))
            gray_image1 = read_image(get_resource_path('imagem1_gray.jpg'))
            plot_histograms_side_by_side(image1, gray_image1, 
                                         titles=['Histograma Imagem1', 'Histograma Imagem Cinza'])
            print("Histograma da Imagem1 e da Imagem Cinza foram exibidos lado a lado.")

        elif choice == '0':
            print("Saindo...")
            break

        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
