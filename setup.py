from setuptools import setup, find_packages

import os

setup(
    name='cardpy',
    version='2.0.3',
    packages=find_packages(),
    install_requires=[],
    author='Risheet Lenka',
    author_email='risheetlenka@gmail.com',
    description='A Python module for playing cards.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/aAa1928/cardpy',
    project_urls={
        'Source': 'https://www.github.com/aAa1928/cardpy',
        'PyPI': 'https://pypi.org/project/cardpy/',
        },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
