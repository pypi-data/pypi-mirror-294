from setuptools import setup, find_packages

setup(
    name="LSS_dplona", 
    version="1.1.4", 
    author="Dawid Plona",
    author_email="dawid.plona@jumbomaritime.nl",
    description="A package for handling Limiting Sea States simulations automatically",
    packages=find_packages(include=['LSS_dplona', 'LSS_dplona.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "numpy",
        "requests",
        "pandas",
        "pyyaml",
        "openpyxl",
        "psutil",
        "OrcFxAPI",
    ],
)
