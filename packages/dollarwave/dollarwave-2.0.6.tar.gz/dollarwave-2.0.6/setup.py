from setuptools import setup, find_packages
import warnings

# Add a warning to notify users when they install or use the package
warnings.warn(
    "This package is deprecated and will no longer be maintained. "
    "Please use 'quantsumore' instead.",
    DeprecationWarning
)

# Read README.md with utf-8 encoding
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dollarwave',
    version="2.0.6",  
    author='Cedric Moore Jr.',
    author_email='cedricmoorejunior5@gmail.com',
    description=(
        '⚠️ DEPRECATED: This package is no longer maintained. '
        'Please use quantsumore instead. A comprehensive Python library for scraping and retrieving real-time data across multiple financial markets, including cryptocurrencies, equities, Forex, treasury yields, and consumer price index (CPI) data.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cedricmoorejr/dollarwave/tree/v2.0.6',
    project_urls={
        'Source Code': 'https://github.com/cedricmoorejr/dollarwave/releases/tag/v2.0.6',
        'New Library': 'https://pypi.org/project/quantsumore',  # Link to the new library
    },
    packages=find_packages(),
    package_data={
        'dollarwave': ['assets/*.ico', 'assets/*.png'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 7 - Inactive',  # Mark the project as inactive
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'requests',
        'matplotlib',
        'pillow',
    ],
    license='MIT',
    include_package_data=True,
)
