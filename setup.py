from setuptools import setup, find_packages

import os

setup(
    name='cardpy',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],
    author='Risheet Lenka',
    author_email='risheetlenka@gmail.com',
    description='A Python module for playing cards.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/aAa1928/cardpy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
