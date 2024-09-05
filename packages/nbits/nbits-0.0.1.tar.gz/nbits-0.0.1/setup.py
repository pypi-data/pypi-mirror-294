from setuptools import setup, find_packages

setup(
    name='nbits',
    version='0.0.1',
    author='SlightwindSec',
    author_email='slightwindsec@gmail.com',
    description='description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SlightwindSec/nbits',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',  # Python 版本要求
    install_requires=[],
)
