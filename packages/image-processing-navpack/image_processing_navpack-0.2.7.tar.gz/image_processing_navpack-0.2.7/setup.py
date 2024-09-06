from setuptools import setup, find_packages

setup(
    name='image_processing_navpack',
    version='0.2.7',  # Atualize a versão aqui
    description='A package for processing and analyzing images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fabiano',
    author_email='nav.info.suporte@gmail.com',
    license='MIT',
    packages=find_packages(include=['image_processing', 'image_processing.*']),
    install_requires=[
        'numpy>=1.26.4',
        'matplotlib>=3.9.2',
        'scikit-image>=0.24.0',
        'imageio>=2.35.1'
    ],
    extras_require={
        'dev': ['pytest>=8.3.2']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'image-processing=image_processing.tests.test_image:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={
        'Source': 'https://github.com/Fabianonavarro/image_processing_navpack.git',
        'Documentation': 'https://github.com/Fabianonavarro/image_processing_navpack/blob/main/README.md',
    }
)
