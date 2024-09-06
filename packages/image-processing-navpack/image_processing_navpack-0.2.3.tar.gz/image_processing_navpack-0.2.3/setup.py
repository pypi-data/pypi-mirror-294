from setuptools import setup, find_packages

setup(
    name='image_processing_navpack',  # Nome do pacote
    version='0.2.3',  # Versão do pacote
    description='A package for processing and analyzing images.',  # Descrição curta do pacote
    long_description=open('README.md').read(),  # Descrição longa do pacote, lida do README.md
    long_description_content_type='text/markdown',  # Tipo de conteúdo do README.md
    author='Fabiano',  # Nome do autor
    author_email='nav.info.suporte@gmail.com',  # Email do autor
    license='MIT',  # Licença do pacote
    packages=find_packages(include=['image_processing', 'image_processing.*']),  # Encontrar pacotes automaticamente
    install_requires=[  # Dependências do pacote
        'numpy>=1.26.4',
        'matplotlib>=3.9.2',
        'scikit-image>=0.24.0',
        'imageio>=2.35.1'
    ],
    extras_require={  # Dependências adicionais para desenvolvimento
        'dev': ['pytest>=8.3.2']
    },
    include_package_data=True,  # Incluir arquivos adicionais especificados no MANIFEST.in
    entry_points={  # Definir pontos de entrada para scripts de linha de comando
        'console_scripts': [
            'image-processing=image_processing.tests.test_image:main'  # Modificado para o script correto
        ]
    },
    classifiers=[  # Classificações do pacote
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={  # Links para o projeto
        'Source': 'https://github.com/Fabianonavarro/image_processing_navpack.git',
        'Documentation': 'https://github.com/Fabianonavarro/image_processing_navpack/blob/main/README.md',
    }
)