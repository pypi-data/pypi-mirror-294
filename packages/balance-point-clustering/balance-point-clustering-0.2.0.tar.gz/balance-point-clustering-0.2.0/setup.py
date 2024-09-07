
### 3. `setup.py`

from setuptools import setup, find_packages

setup(
    name="balance-point-clustering",
    version="0.2.0",  # Incremented version to reflect new features
    description="A Python package for Balance Point Clustering with dynamic cluster determination.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Sathya Narayanan",
    author_email="impssn@gmail.com",
    url="https://github.com/Impssn/Balance-Point-Clustering.git",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
