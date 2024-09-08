from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = "A library for processing and plotting EEG data"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='eeg_analysis',
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Karthik Dani',
    author_email='karthikdani14@gmail.com',
    url='https://github.com/KarthikDani/PHCCOProject/tree/main/gsmm',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'eeg_analysis': ['data/*.csv'],
    },
    license='MIT',
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'load_clean_and_plot=eeg_analysis.main:load_clean_and_plot',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.7'
    )