# setup.py
from setuptools import setup, find_packages

print(find_packages(where='src')) 

setup(
    name='gs-api-wrapper',               # Name of the package
    version='1.0.1',                     # Package version
    description='A Python wrapper for GoldenSource API',  # Short description
    author='Nasar Qadir',                  # Your name or organization
    author_email='nqadir@thegoldensource.com',  # Your email
    url='https://github.com/nqadirgs/gs-api-wrapper',  # Project URL or repository
    packages=find_packages(where='src'), # Automatically find packages in src/
    package_dir={'': 'src'},             # Base directory for packages
    install_requires=[
        'requests>=2.25.0',              # Dependencies (if you have any)
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose the appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',             # Python version compatibility
)
