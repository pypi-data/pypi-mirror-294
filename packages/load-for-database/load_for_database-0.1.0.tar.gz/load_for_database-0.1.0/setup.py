from setuptools import setup, find_packages

setup(
    name="load_for_database",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sqlalchemy",
        "pyodbc",
    ],
    author="Lucas Bononi",
    author_email="contatobononi@gmail.com",
    description="Function to load data from XLSX files to a SQL Server database",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bononi48/load_for_database.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
