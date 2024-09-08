from setuptools import setup, find_packages

setup(
    name='lens_v1',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='A package for extracting named entities in skin cancer narratives using a pre-trained NER model.',
    author='Daisy Monika Lal',
    author_email='d.m.lal@lancaster.ac.uk',
    license='MIT',
    install_requires=[
        'transformers>=4.0.0',
        'torch>=1.7.0',
        'spacy>=3.0.0',
        'pandas>=1.0.0',
        'numpy>=1.19.0',
        'spacy-transformers>=1.0.0',
    ],
    package_data={
        '': ['model-v2/*'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
