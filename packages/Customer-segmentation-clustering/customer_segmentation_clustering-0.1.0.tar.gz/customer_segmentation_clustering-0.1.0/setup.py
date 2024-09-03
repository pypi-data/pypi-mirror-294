from setuptools import setup, find_packages

setup(
    name='Customer_segmentation_clustering',
    version='0.1.0',
    packages=find_packages(),
    author='Phalguni',
    author_email='phalgunishenoy2002@gmail.com',
    description='A data analysis package for preprocessing data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
